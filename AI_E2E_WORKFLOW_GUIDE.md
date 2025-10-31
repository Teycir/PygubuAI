# AI End-to-End Workflow Testing Guide

## Overview

Complete test suite for AI integration with Amazon Q, covering the full workflow from project creation to AI-powered analysis and suggestions.

## Test Files

### 1. test_ai_integration.py
Basic AI module tests with simple fixtures.

**Coverage:**
- Context generation
- Project analysis
- Refactoring suggestions
- Natural language queries

**Fixtures:**
- temp_ai_project (2 widgets)
- temp_complex_project (8+ widgets)

### 2. test_ai_realworld.py
Production-quality application tests.

**Coverage:**
- CRM application (25+ widgets)
- Settings dialog (20+ widgets)
- Analytics dashboard (20+ widgets)
- Data entry form (15+ widgets)
- File browser (15+ widgets)

**Tests:**
- Complex UI analysis
- Refactoring suggestions for real patterns
- Context generation with rich metadata
- Natural language queries on production UIs

### 3. test_ai_e2e_workflow.py
Complete end-to-end workflow tests.

**Coverage:**
- Full workflow: Create -> Analyze -> Query -> Refactor -> Context
- Project modifications and re-analysis
- Multi-project comparison
- Error handling
- Performance with large projects (50+ widgets)

## Running Tests

### Quick Start
```bash
# Install dependencies
pip install -e '.[dev]'

# Run all AI tests
./run_ai_tests.sh
```

### Individual Test Suites
```bash
# Basic tests
pytest tests/test_ai_integration.py -v

# Real-world tests
pytest tests/test_ai_realworld.py -v

# End-to-end workflows
pytest tests/test_ai_e2e_workflow.py -v
```

### With Coverage
```bash
pytest tests/test_ai_*.py \
  --cov=pygubuai.ai_analyzer \
  --cov=pygubuai.ai_context \
  --cov=pygubuai.ai_query \
  --cov=pygubuai.ai_refactor \
  --cov-report=html
```

## Workflow Tests Explained

### test_complete_ai_workflow_crm
Simulates complete Amazon Q integration:

1. **Project Analysis** - Analyze CRM app structure
2. **Natural Language Queries** - Ask about widgets, callbacks, complexity
3. **Refactoring Suggestions** - Get improvement recommendations
4. **Context Generation** - Create rich context for AI chat
5. **Format for AI** - Convert to Amazon Q-friendly format

**Validates:**
- All modules work together
- Data flows correctly between components
- Output is suitable for AI consumption

### test_workflow_with_modifications
Tests dynamic project updates:

1. **Initial Analysis** - Baseline metrics
2. **Modify UI** - Add widgets programmatically
3. **Re-analyze** - Detect changes
4. **Update Suggestions** - New recommendations

**Validates:**
- Change detection works
- Metrics update correctly
- Suggestions adapt to changes

### test_multi_project_workflow
Tests cross-project analysis:

1. **Analyze Multiple Projects** - Simple, medium, complex
2. **Compare Complexity** - Relative scoring
3. **Generate Contexts** - For each project

**Validates:**
- Registry handles multiple projects
- Complexity scoring is relative
- Context generation scales

### test_error_handling_workflow
Tests failure scenarios:

1. **Non-existent Project** - Graceful error handling
2. **Invalid Queries** - Proper error messages
3. **Missing Files** - Fallback behavior

**Validates:**
- No crashes on errors
- Helpful error messages
- Graceful degradation

### test_performance_large_project
Tests scalability:

1. **Generate Large Project** - 50+ widgets
2. **Measure Analysis Time** - Should be < 2 seconds
3. **Measure Context Time** - Should be < 2 seconds

**Validates:**
- Performance at scale
- No memory issues
- Fast enough for interactive use

## Expected Results

### Success Criteria

All tests should pass with:
- Analysis completes in < 2 seconds
- Context generation in < 2 seconds
- Correct widget counts
- Appropriate complexity scores
- Relevant suggestions
- Proper error handling

### Sample Output

```
test_ai_integration.py::test_ai_context_generation PASSED
test_ai_integration.py::test_ai_analyzer_metrics PASSED
test_ai_integration.py::test_ai_refactor_suggestions PASSED
test_ai_integration.py::test_ai_query_widgets PASSED
test_ai_integration.py::test_ai_query_callbacks PASSED
test_ai_integration.py::test_ai_query_complexity PASSED
test_ai_integration.py::test_ai_analyzer_complex_ui PASSED
test_ai_integration.py::test_ai_query_specific_widgets PASSED
test_ai_integration.py::test_ai_context_with_metadata PASSED

test_ai_realworld.py::test_crm_application_analysis PASSED
test_ai_realworld.py::test_settings_dialog_refactoring PASSED
test_ai_realworld.py::test_dashboard_context_generation PASSED
test_ai_realworld.py::test_data_entry_form_queries PASSED
test_ai_realworld.py::test_file_browser_complexity PASSED

test_ai_e2e_workflow.py::test_complete_ai_workflow_crm PASSED
test_ai_e2e_workflow.py::test_workflow_with_modifications PASSED
test_ai_e2e_workflow.py::test_multi_project_workflow PASSED
test_ai_e2e_workflow.py::test_error_handling_workflow PASSED
test_ai_e2e_workflow.py::test_performance_large_project PASSED

======================== 24 passed in 5.23s ========================
```

## Integration with Amazon Q

### How Tests Simulate Amazon Q Workflow

1. **User Creates Project**
   - `pygubu-create myapp 'description'`
   - Project registered

2. **User Opens Amazon Q Chat**
   - "Analyze my pygubu project"
   - AI calls `analyze_project()`

3. **User Asks Questions**
   - "How many widgets do I have?"
   - AI calls `query_project()`

4. **User Requests Suggestions**
   - "What can I improve?"
   - AI calls `analyze_refactoring_opportunities()`

5. **Context Loaded Automatically**
   - `@pygubu-context` prompt
   - AI calls `generate_context()`

### Real Amazon Q Commands

```python
# In Amazon Q chat:
"Analyze my CRM project"
# -> Calls ai_analyzer.analyze_project('crm')

"How many buttons in my dashboard?"
# -> Calls ai_query.query_project('dashboard', 'How many buttons?')

"What should I refactor in settings dialog?"
# -> Calls ai_refactor.analyze_refactoring_opportunities('settings_dialog')

"Show me project context"
# -> Calls ai_context.generate_context('myproject')
```

## Troubleshooting

### Tests Fail with ImportError
```bash
pip install -e .
```

### Tests Fail with "pytest not found"
```bash
pip install -e '.[dev]'
```

### Slow Performance
Check if running with coverage enabled. Disable for faster runs:
```bash
pytest tests/test_ai_e2e_workflow.py -v  # No coverage
```

### Registry Errors
Tests use temporary registries. If issues persist:
```bash
rm -rf /tmp/pytest-*
```

## Next Steps

1. **Run Tests** - Verify all pass
2. **Check Coverage** - Aim for 90%+
3. **Add Custom Tests** - For your specific use cases
4. **Integrate with CI** - Add to GitHub Actions

## Contributing

When adding new AI features:

1. Add unit tests to `test_ai_integration.py`
2. Add real-world test to `test_ai_realworld.py`
3. Add workflow test to `test_ai_e2e_workflow.py`
4. Update this guide

## Resources

- [AI Module Documentation](src/pygubuai/ai_*.py)
- [Testing Quick Reference](TESTING_QUICK_REF.md)
- [Amazon Q Integration](README.md#ai-chat-integration)
