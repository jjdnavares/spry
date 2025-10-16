# Writer Module

The Writer module provides AI-powered content generation capabilities within Spry using Frappe DocTypes.

## Features

- **AI-powered content generation** - Generate content using various LLM providers
- **Content management** - Full CRUD operations via Frappe DocType
- **Analytics & reporting** - Track content generation trends and metrics
- **Multi-provider support** - Designed to work with OpenAI, Anthropic, Google, and more
- **User permissions** - Role-based access control
- **Content versioning** - Track changes automatically

## Structure

```
writer/
├── doctype/
│   └── generated_content/      # Main DocType for content storage
│       ├── generated_content.json
│       ├── generated_content.py
│       ├── generated_content.js
│       ├── generated_content_list.js
│       ├── test_generated_content.py
│       └── README.md
├── api/
│   ├── permission.py           # Permission utilities
│   └── content.py              # Content generation APIs
├── fixtures/                   # Sample data (future use)
└── templates/                  # Jinja templates (future use)
```

## Getting Started

### Installation

The Writer module is automatically installed with Spry. After installation:

1. Run migrations: `bench --site [site-name] migrate`
2. Clear cache: `bench --site [site-name] clear-cache`
3. Access via `/app/generated-content` or create a workspace in the UI

### Quick Start

1. **Access the Writer workspace** - Click "Writer" in the app screen
2. **Create new content** - Click "New Content" shortcut
3. **Fill in the form**:
   - Title: Descriptive title for your content
   - Prompt: Instructions for content generation
   - Keyword: Main keyword/topic
   - Tone: Desired tone (professional, casual, etc.)
   - Provider: LLM provider (OpenAI, Anthropic, etc.)
   - Model: Specific model to use
4. **Save** - The content is stored and tracked

### API Usage

```python
import frappe

# Generate content
result = frappe.call(
    "spry.writer.api.content.generate_content",
    prompt="Write an article about AI",
    keyword="artificial intelligence",
    tone="professional",
    provider="OpenAI",
    model="gpt-4",
    content_type="Article"
)

# Get content list
content_list = frappe.call(
    "spry.writer.api.content.get_content_list",
    limit=20
)

# Get specific content
content = frappe.call(
    "spry.writer.api.content.get_content_detail",
    name="GC-2025-00001"
)
```

## Components

### DocType: Generated Content

Stores all AI-generated content with the following fields:
- **Title** - Content title
- **Prompt** - Generation prompt
- **Generated Text** - The actual content
- **Keyword** - Main keyword
- **Tone** - Content tone
- **Provider** - LLM provider used
- **Model** - Model name
- **Content Type** - Type of content
- **User** - Creator

### Dashboard Charts

1. **Content Generation Trends** - Line chart showing content creation over time
2. **Content by Provider** - Donut chart showing distribution by LLM provider

### Reports

**Content Analytics** - Comprehensive report showing:
- Content details
- Word counts
- Provider usage
- User activity
- Filterable by date, provider, content type, user, and keyword

## Permissions

Configure permissions via Role Permission Manager:
- Default: System Manager has full access
- Customize for other roles as needed
- Permission check: `has_writer_permission()`

## Integration

### LLM Provider Integration

To integrate actual LLM providers, implement the generation logic in:
`spry/writer/api/content.py` → `generate_content()` function

Example integration points:
- OpenAI API
- Anthropic Claude
- Google Gemini
- Local models (Ollama, etc.)

### Extending Functionality

1. **Add new fields** - Modify `generated_content.json`
2. **Custom validation** - Update `generated_content.py`
3. **Client-side logic** - Modify `generated_content.js`
4. **New API endpoints** - Add to `api/content.py`

## Best Practices

1. **Use descriptive titles** - Makes content easy to find
2. **Track your prompts** - Good prompts can be reused
3. **Review generated content** - Always review before publishing
4. **Set appropriate permissions** - Control who can create/edit content
5. **Monitor analytics** - Use reports to track usage patterns

## Troubleshooting

### Permission Issues
- Check user roles in User doctype
- Verify role permissions in Role Permission Manager
- Ensure `has_writer_permission()` returns True

### Content Not Saving
- Check required fields are filled
- Review validation errors in console
- Verify database connectivity

### Workspace Not Showing
- Run `bench --site [site] migrate`
- Clear cache: `bench --site [site] clear-cache`
- Check workspace is public and not hidden

## Future Enhancements

- [ ] Real-time LLM integration
- [ ] Content templates and presets
- [ ] Batch content generation
- [ ] Content scheduling
- [ ] SEO optimization tools
- [ ] Multi-language support
- [ ] Content collaboration features
- [ ] Version comparison
- [ ] Export to various formats

## Documentation

- [Usage Guide](USAGE.md) - Detailed usage instructions
- [DocType README](doctype/generated_content/README.md) - DocType documentation
- [API Reference](api/) - API endpoint documentation

## Support

For issues or questions:
1. Check the documentation
2. Review error logs in Error Log doctype
3. Contact system administrator
