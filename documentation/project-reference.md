# Project Reference and Scope

## Official project title

**Serverless E-Commerce Order Processing System on AWS**

## Business problem

The project document describes an e-commerce application with a significant increase in incoming requests on Fridays. The stated risks are slow application responses, overloaded services, failed requests, and delayed order processing. The central challenge is to handle increasing traffic automatically without manually adding servers.

## Objectives

- Build a scalable serverless application.
- Handle increased traffic using AWS managed services.
- Allow customers to create and track orders.
- Process background operations asynchronously.
- Deliver customer notifications.
- Improve reliability and monitoring.

## Scope stated in the supplied PDF

- Order creation and retrieval.
- Simulated payment processing.
- Event-driven background processing.
- Asynchronous messaging using Amazon SQS.
- Customer notifications using Amazon SNS.
- Security and monitoring using IAM and CloudWatch.
- Infrastructure deployment using Terraform.

Out of scope in the supplied PDF: real payment-gateway integration, inventory management, and frontend development.

## Documented architecture workflow

1. The customer submits an order through API Gateway.
2. CreateOrderFn stores the order in DynamoDB.
3. The system immediately returns an order ID to the customer.
4. DynamoDB Streams triggers ProcessPaymentFn.
5. The function simulates payment processing and updates the order.
6. The Transactional Outbox Pattern records the business event in the same database transaction.
7. OutboxDispatcherFn publishes the event to SQS.
8. NotifyCustomerFn consumes the message and publishes a notification through SNS.
9. SNS delivers the notification to the customer.

## Chapter plan in the supplied PDF

1. Project Overview and Business Requirements
2. System Architecture and Design Decisions
3. AWS Services Selection and Comparison
4. API Layer — Amazon API Gateway
5. Order Management — AWS Lambda and DynamoDB
6. Event-Driven Processing — DynamoDB Streams
7. Reliable Messaging — Transactional Outbox Pattern
8. Asynchronous Communication — Amazon SQS
9. Customer Notifications — Amazon SNS
10. Security and IAM Least-Privilege Design
11. Monitoring, Logging, and Troubleshooting
12. End-to-End Testing and Validation
13. Infrastructure as Code — Terraform
14. Architecture Limitations and Future Improvements
15. Final Architecture, Lessons Learned, and References

## Implementation evidence still required

The PDF contains AWS Console screenshots and some code/test evidence, but screenshots alone are not a substitute for source files. The repository should contain the actual Lambda source, event-source mappings, IAM policies, DynamoDB key/stream settings, SQS redrive configuration, SNS subscription details, test events/results, and Terraform files where implemented.

Each item must be marked as one of:
- **Implemented and verified** — supported by source/configuration and a successful test or console result.
- **Implemented, not yet validated** — configured but no successful end-to-end evidence yet.
- **Planned** — described in the design but not yet implemented.
- **Blocked/failed** — an attempted setup that did not complete successfully.

## Validation caveat

The PDF describes an architecture intended to accommodate traffic variations and explicitly says actual capacity must be validated through load testing. Do not describe a target request rate as proven capacity unless repeatable load-test results support it.