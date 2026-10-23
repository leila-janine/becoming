import {loadPyodide} from 'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs';

const ready=loadPyodide({indexURL:'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/'});
const sqlProgram=String.raw`
import sqlite3, json
connection=sqlite3.connect(':memory:')
try:
    connection.executescript(_setup)
    buffer=''
    results=[]
    statements=[]
    for char in _script:
        buffer+=char
        if char==';' and sqlite3.complete_statement(buffer):
            statements.append(buffer)
            buffer=''
    if buffer.strip():
        statements.append(buffer)
    for statement in statements:
        cursor=connection.execute(statement)
        if cursor.description:
            columns=[col[0] for col in cursor.description]
            rows=cursor.fetchmany(1001)
            results=rows
            print(' | '.join(columns))
            for row in rows[:1000]:
                print(' | '.join(str(v) for v in row))
            if len(rows)>1000:
                print('Output limited to 1,000 rows.')
    if _run_checks:
        expected=json.loads(_expected)
        assert [list(row) for row in results]==expected, 'Result does not match the expected rows and order. Include users with no transactions.'
        print('Checks passed')
finally:
    connection.close()
`;

self.onmessage=async event=>{
  let text='',namespace;
  const append=line=>{if(text.length<20000)text+=(String(line)+'\n').slice(0,20000-text.length);};
  try {
    const pyodide=await ready;
    pyodide.setStdout({batched:append});pyodide.setStderr({batched:append});
    pyodide.setStdin({stdin:()=>{throw new Error('Interactive input() is not supported. Set your input values in the code.');}});
    namespace=pyodide.toPy({__name__:'__main__'});
    self.postMessage({type:'executing'});
    const data=event.data;
    if(data.language==='sql') {
      namespace.set('_setup',data.setup||'');namespace.set('_script',data.code);
      namespace.set('_run_checks',!!data.runChecks);namespace.set('_expected',JSON.stringify(data.expected));
      await pyodide.runPythonAsync(sqlProgram,{globals:namespace});
    }else {
      const code=data.code+(data.runChecks?'\n\n'+data.checks:'');
      const result=await pyodide.runPythonAsync(code,{globals:namespace});
      if(result!==undefined&&result!==null){append(String(result));if(result.destroy)result.destroy();}
    }
    self.postMessage({type:'result',ok:true,output:text});
  }catch(error){self.postMessage({type:'result',ok:false,output:text+'\n'+String(error.message||error).slice(0,6000)});}
  finally{if(namespace)namespace.destroy();}
};
