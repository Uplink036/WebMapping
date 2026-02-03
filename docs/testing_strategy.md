# Testing Strategy

## Testing Matrix

| Component / Impact of Fault | Low | Medium | High |
|-----------|-----|--------|------|
| **Frontend** | Manual tests | Manual tests  | Unit Tests |
| **Database** | Manual tests | Manual tests | Unit Tests |
| **API Calls** | Manual tests | Unit tests | Integration tests |
| **Crawler** | Manual tests | Unit tests | System tests |
| **Plugins** | Manual tests | Unit tests | Integration tests |

## Current Implementation

- **Low**: Unit tests for core functions
- **Medium**: Integration tests for database operations
- **High**: Not implemented

## Test Commands

```bash
make tests    # Run all tests
pytest        # Run pytest directly
```
