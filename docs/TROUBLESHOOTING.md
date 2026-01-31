# Troubleshooting Guide

Common issues and their solutions when working with nano_banana.

## Authentication Issues

### Issue: "Invalid access token" error

**Symptoms:**
```
Error: Failed to initialize MLflow experiment: 403: Invalid access token
```

**Solutions:**

1. **Check token expiration:**
```bash
databricks auth token --profile=<your-profile>
```

2. **Refresh authentication:**
```bash
databricks auth login <workspace-url> --profile=<profile-name>
```

3. **Update .env file:**
```bash
# Get fresh token
databricks auth token --profile=<profile> | jq -r .access_token

# Update DATABRICKS_TOKEN in .env
```

4. **Verify workspace URL:**
Ensure `DATABRICKS_HOST` in `.env` matches your authenticated profile.

### Issue: "No valid profile" error

**Symptoms:**
```
Error: No valid Databricks profile found
```

**Solutions:**

1. **List available profiles:**
```bash
databricks auth profiles
```

2. **Create new profile:**
```bash
databricks auth login <workspace-url> --profile=<profile-name>
```

3. **Set default profile in config:**
Update `configs/default.yaml` with correct profile settings.

## API and Model Issues

### Issue: 503 "Model is overloaded" error

**Symptoms:**
```
Error: Image generation failed: 503 UNAVAILABLE
The model is overloaded. Please try again later.
```

**Solutions:**

1. **Wait and retry:**
```bash
sleep 30 && uv run nano-banana generate [your-options]
```

2. **Reduce request frequency:**
Add delays between batch generations:
```bash
for spec in *.yaml; do
    uv run nano-banana generate --diagram-spec "$spec" --template baseline
    sleep 60  # Wait between requests
done
```

3. **Use different model:**
Edit `configs/default.yaml`:
```yaml
vertex:
  model_id: "gemini-1.5-pro"  # Try alternative model
```

### Issue: 400 "Invalid API key" error

**Symptoms:**
```
Error: 400 Bad Request - Invalid API key
```

**Solutions:**

1. **Verify API key:**
```bash
echo $GEMINI_API_KEY
```

2. **Get new API key:**
- Visit https://makersuite.google.com/app/apikey
- Generate new key
- Update `.env` file

3. **Check key format:**
API keys should start with `AIza...`

### Issue: Generation takes too long or times out

**Symptoms:**
- Process hangs for several minutes
- Timeout errors

**Solutions:**

1. **Reduce prompt complexity:**
- Simplify component descriptions
- Reduce number of components
- Use shorter, clearer instructions

2. **Lower temperature:**
```yaml
vertex:
  temperature: 0.4  # Down from 0.7
```

3. **Reduce candidate count:**
```yaml
vertex:
  candidate_count: 1  # Down from 3
```

## Logo Issues

### Issue: Logos not appearing in diagram

**Symptoms:**
- Generated diagram is missing logos
- Only text labels appear

**Solutions:**

1. **Verify logo paths:**
```bash
ls -la logos/default/
```

2. **Check logo kit configuration:**
Edit your diagram spec to ensure logos are specified:
```yaml
components:
  - id: "databricks"
    logo_name: "databricks-full"  # Must match file in logos/default/
```

3. **Validate logos:**
```bash
uv run nano-banana validate-logos --logo-dir logos/default/
```

### Issue: Logo filenames appearing in diagram

**Symptoms:**
- Diagram shows "databricks-full.png" instead of just the logo
- Filenames visible in output

**Solutions:**

1. **Update prompt template:**
Ensure logo constraints are included. Prompts should use descriptions, not filenames.

2. **Check logos.py mappings:**
Verify logo descriptions are properly defined in `src/nano_banana/logos.py`.

3. **Use guaranteed constraints:**
The system should auto-inject logo constraints. If not, update prompts.

### Issue: Poor logo quality or wrong colors

**Symptoms:**
- Logos appear blurry or pixelated
- Colors don't match brand guidelines

**Solutions:**

1. **Use high-resolution logos:**
- Minimum 500x500 pixels
- PNG format with transparency preferred
- Official brand assets only

2. **Check logo file:**
```bash
file logos/default/databricks-full.png
identify logos/default/databricks-full.png  # requires imagemagick
```

3. **Replace with official version:**
Download from official brand resources.

## Output Issues

### Issue: Diagram layout is messy or unclear

**Symptoms:**
- Components overlap
- Flow direction is unclear
- Spacing is inconsistent

**Solutions:**

1. **Be more explicit in prompt:**
```
"Arrange components left-to-right in three clear columns:
- Left: Data sources
- Center: Processing layer with Databricks
- Right: Data consumers"
```

2. **Use different template:**
```bash
# Try minimal for simpler layouts
uv run nano-banana generate --template minimal [other-options]
```

3. **Reduce component count:**
Break complex diagrams into multiple simpler ones.

### Issue: Text is too small or unreadable

**Symptoms:**
- Labels too small when viewing diagram
- Text appears cut off

**Solutions:**

1. **Specify text requirements in prompt:**
```
"Use large, easily readable labels with sentence case.
Ensure all text is clearly legible."
```

2. **Request larger canvas:**
```
"Create diagram on large canvas with ample spacing for readability."
```

3. **Reduce information density:**
Show fewer components or split into multiple diagrams.

### Issue: Colors don't match branding

**Symptoms:**
- Wrong color scheme
- Inconsistent with brand guidelines

**Solutions:**

1. **Specify colors explicitly:**
```
"Use Databricks color palette:
- Primary: #FF3621 (red)
- Secondary: #00A972 (green)
- Background: white"
```

2. **Use branding files:**
```bash
uv run nano-banana generate-raw \
    --prompt-file prompts/my_prompt.txt \
    --branding prompts/branding/databricks.txt  # If feature exists
```

3. **Reference examples:**
Include links to reference diagrams with desired styling.

## MLflow and Tracking Issues

### Issue: Experiment not found

**Symptoms:**
```
Error: Experiment not found
```

**Solutions:**

1. **Check experiment name:**
Verify in `configs/default.yaml`:
```yaml
mlflow:
  experiment_name: "/Users/your.email@databricks.com/nano-banana"
```

2. **Create experiment manually:**
In Databricks workspace:
- Navigate to ML → Experiments
- Create experiment with matching path

3. **Check permissions:**
Ensure you have write access to the MLflow experiment location.

### Issue: Artifacts not uploading

**Symptoms:**
- Run completes but artifacts missing
- Error messages about S3/Azure storage

**Solutions:**

1. **Check artifact location:**
```yaml
mlflow:
  artifact_location: "dbfs:/databricks/mlflow-tracking/<experiment-id>"
```

2. **Verify workspace permissions:**
Ensure you can write to DBFS/cloud storage.

3. **Check network connectivity:**
Some corporate networks block cloud storage access.

## File and Path Issues

### Issue: "File not found" errors

**Symptoms:**
```
Error: Could not find file: prompts/my_spec.yaml
```

**Solutions:**

1. **Check current directory:**
```bash
pwd  # Should be in /path/to/bricksmith
ls prompts/diagram_specs/
```

2. **Use absolute paths:**
```bash
uv run nano-banana generate \
    --diagram-spec /full/path/to/spec.yaml
```

3. **Verify file exists:**
```bash
ls -la prompts/diagram_specs/my_spec.yaml
```

### Issue: Permission denied errors

**Symptoms:**
```
Error: Permission denied: outputs/
```

**Solutions:**

1. **Check directory permissions:**
```bash
ls -ld outputs/
chmod 755 outputs/
```

2. **Create outputs directory:**
```bash
mkdir -p outputs
```

3. **Run with appropriate permissions:**
May need to adjust file ownership or run in different directory.

## Installation and Environment Issues

### Issue: "Command not found: nano-banana"

**Symptoms:**
```bash
nano-banana: command not found
```

**Solutions:**

1. **Use uv run:**
```bash
uv run nano-banana [command]
```

2. **Activate virtual environment:**
```bash
source .venv/bin/activate
nano-banana [command]
```

3. **Reinstall package:**
```bash
uv pip install -e .
```

### Issue: Import errors or missing dependencies

**Symptoms:**
```
ModuleNotFoundError: No module named 'google.generativeai'
```

**Solutions:**

1. **Reinstall dependencies:**
```bash
uv pip install -e .
```

2. **Check Python version:**
```bash
python --version  # Should be 3.12+
```

3. **Clean and reinstall:**
```bash
rm -rf .venv
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Issue: uv not found

**Symptoms:**
```
command not found: uv
```

**Solutions:**

1. **Install uv:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Add to PATH:**
```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

3. **Verify installation:**
```bash
uv --version
```

## Configuration Issues

### Issue: Config not loading

**Symptoms:**
- Settings from YAML not applied
- Using default values instead

**Solutions:**

1. **Verify config file path:**
```bash
cat configs/default.yaml
```

2. **Check YAML syntax:**
```bash
python -c "import yaml; yaml.safe_load(open('configs/default.yaml'))"
```

3. **Use explicit config:**
```bash
uv run nano-banana generate --config configs/local.yaml [other-options]
```

### Issue: Environment variables not working

**Symptoms:**
- Settings in .env not being used
- Still getting errors after updating .env

**Solutions:**

1. **Source .env file:**
```bash
source .env
echo $GEMINI_API_KEY  # Verify it's set
```

2. **Export manually:**
```bash
export GEMINI_API_KEY="your-key-here"
export DATABRICKS_HOST="https://..."
```

3. **Check .env format:**
Ensure no extra spaces or quotes:
```bash
GEMINI_API_KEY=AIza...
DATABRICKS_HOST=https://adb-...
```

## Performance Issues

### Issue: Generation is very slow

**Symptoms:**
- Takes 2-3+ minutes per diagram
- Much slower than expected

**Solutions:**

1. **Simplify prompt:**
- Reduce component count
- Shorten descriptions
- Remove unnecessary details

2. **Optimize model settings:**
```yaml
vertex:
  temperature: 0.5
  top_p: 0.9
  top_k: 40
  candidate_count: 1
```

3. **Check network:**
Slow network can impact API calls significantly.

### Issue: High API costs

**Symptoms:**
- Large API bills
- Many tokens consumed

**Solutions:**

1. **Optimize prompts:**
- Remove redundant information
- Use concise descriptions
- Reference templates instead of repeating content

2. **Reduce iterations:**
- Get prompt right before generating
- Use evaluation to iterate systematically
- Learn from previous runs

3. **Monitor usage:**
Track API usage in MLflow and Google Cloud Console.

## Getting More Help

### Check Logs
```bash
# View recent MLflow runs
uv run nano-banana list-runs

# Check specific run details
uv run nano-banana show-run <run-id>
```

### Enable Debug Mode
```bash
export LOG_LEVEL=DEBUG
uv run nano-banana [command]
```

### Common Debug Commands
```bash
# Verify setup
uv run nano-banana verify-setup

# Check authentication
uv run nano-banana check-auth

# Validate logos
uv run nano-banana validate-logos --logo-dir logos/default/

# List available templates
ls prompts/prompt_templates/
```

### Report Issues
When reporting issues, include:
1. Full error message
2. Command that failed
3. Config settings (redact secrets)
4. Python version and OS
5. Recent log output

### Community Resources
- Project README: `/README.md`
- Documentation: `/docs/`
- Examples: `/prompts/`
- Issue tracker: (if applicable)
