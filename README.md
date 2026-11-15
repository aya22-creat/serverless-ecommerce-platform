# Serverless E-Commerce Order Processing System on AWS

A serverless, event-driven e-commerce order-processing project designed to handle variable request volume, including recurring Friday traffic spikes.

> **Project status:** The repository was newly created and is being populated from the project documentation and implementation evidence. The current design and scope below are based on the supplied project document. Code and AWS configuration will be added only after they are recovered and verified.

## Business problem

The e-commerce application experiences a significant increase in incoming requests on Fridays. This can lead to slow responses, overloaded services, failed requests, and delayed order processing. The goal is to absorb changing traffic automatically without manually provisioning application servers.

## Objectives

- Build a scalable serverless application.
- Accept new orders and allow customers to retrieve order status.
- Move background work out of the customer-facing request path.
- Process payment events asynchronously (simulated payment only).
- Deliver customer notifications.
- Improve reliability, security, and observability.

## Architecture at a glance

The documented design uses the following flow:

1. A client sends an order request to **Amazon API Gateway**.
2. **CreateOrderFn** stores the order in the **Orders** DynamoDB table and returns an order ID.
3. **DynamoDB Streams** detects the new order and invokes **ProcessPaymentFn**.
4. The payment function simulates payment processing, updates the order, and records the corresponding business event in **OrderOutbox** using the Transactional Outbox approach.
5. **OutboxDispatcherFn** publishes the outbox event to **Amazon SQS**.
6. **NotifyCustomerFn** consumes the message and publishes a notification through **Amazon SNS**.
7. A dead-letter queue isolates messages that repeatedly fail processing.

The API also exposes GET /orders/{orderId} through **GetOrderStatusFn**.

## AWS services in the documented design

| Service | Responsibility |
|---|---|
| Amazon API Gateway | HTTP API entry point |
| AWS Lambda | Order, payment, dispatch, and notification logic |
| Amazon DynamoDB | Orders and outbox event storage |
| DynamoDB Streams | Change-driven processing |
| Amazon SQS | Asynchronous message delivery |
| Amazon SQS DLQ | Isolation of repeatedly failing messages |
| Amazon SNS | Customer notification delivery |
| AWS IAM | Function-specific least-privilege permissions |
| Amazon CloudWatch | Logs and monitoring |
| Terraform | Planned infrastructure-as-code deployment |

## Repository guide

- documentation/ — project chapters, implementation notes, decisions, and troubleshooting.
- architecture/ — architecture diagrams and design decisions.
- src/ — verified Lambda source code, grouped by responsibility.
- infrastructure/ — verified Terraform and IAM/configuration artifacts.
- screenshots/ — implementation evidence from the AWS Console and tests.
- tests/ — repeatable test events and validation material.

These folders will be populated as source artifacts are reviewed. No placeholder code is presented as deployed code.

## Scope and limitations

The supplied project document explicitly excludes real payment-gateway integration, inventory management, and frontend development. Payment processing is simulated. The architecture's ability to handle peak traffic must be validated with load testing; no throughput claim is made here.

## Documentation source

The initial project reference is the supplied Project Title PDF. Its chapter plan covers project requirements, architecture, AWS service selection, API Gateway, order management, DynamoDB Streams, Transactional Outbox, SQS, SNS, IAM, monitoring, end-to-end testing, Terraform, limitations, and lessons learned.

As implementation artifacts are recovered, each chapter will link to the corresponding source code, configuration, screenshots, and test evidence.

## Security note

Never commit AWS access keys, secret values, account credentials, or unredacted sensitive customer data. Replace environment-specific identifiers with documented placeholders where appropriate.