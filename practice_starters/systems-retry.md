# Review a retry that could duplicate a payment

A client sends POST /orders. The server creates the order, but the response times out. The client retries the same request, and a second order is created. Write a short design proposal to prevent duplicate orders while allowing safe retries. Do not use real payment data.

# Safe retry design

## Failure scenario

## Request contract

## Storage and concurrency

## Error handling

## Tests
