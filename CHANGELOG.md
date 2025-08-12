# Changelog

All notable changes to Hexflow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-12

### Added
- Initial release of Hexflow
- Core framework architecture with launcher, router, and state management
- Skeleton system for rapid application development:
  - HTTPBaseApp for all http-based services
  - CasaApp for form-based data collection
  - DisplayApp for read-only confirmation pages
- DAG-based workflow orchestration
- Pluggable state backend system (SQLite backend included)
- Session management with cross-device workflow resumption
- Command-line interface via `hexflow` command
- Complete example workflows:
  - Self-test: Basic three-step demonstration
  - Fishing license: Government service application
  - Employee onboarding: Multi-step HR process
- AI.md guide for AI-driven workflow generation
- Comprehensive documentation and examples