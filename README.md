# Infrastructure Lambdas

Source repository for AWS Lambda functions used in infrastructure projects.

## ami-s3-cleaner

## check-ami-ready

## check-inspector-assessment-run-complete

## launch-instance

## parse-inspector-assessment-run-findings

## send-sns-to-pushover

Basic relay between AWS SNS messages and the 
[Pushover](https://pushover.net/) service. Patterned after the Scopely 
[Slack-SNS](https://github.com/scopely/slack-sns) project.

Expected Environment variables:

- pushover_token: Pushover API Token
- pushover_user: Pushover User ID

## start-inspector-assessment-run

## start-step-function

## tag-ec2-resource

## terminate-instance

# Contributing

This project is governed by a [Code of Conduct](./CODE_OF_CONDUCT.md). 
By participating in this project you agree to abide by these terms.

# License

The [MIT License](LICENSE) applies.
