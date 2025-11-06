CI / CD setup

This project includes a GitHub Actions workflow at `.github/workflows/ci.yml`.

What it does

- On push or PR to `main`/`master`:
  - Installs Python 3.12 and project dependencies
  - Runs `pytest` if a `tests` folder or `pytest.ini` is present
- On push to `main`/`master` (after tests pass):
  - Builds a Docker image
  - Optionally pushes to Docker Hub when secrets are set

Required GitHub secrets for pushing (optional)

- `DOCKERHUB_USERNAME` - your Docker Hub username
- `DOCKERHUB_TOKEN` - Docker Hub access token or password

Notes

- The workflow assumes `requirements.txt` exists (it does).
- Adjust `tags` in the workflow to match your repo/image name.
- For private registries or GitHub Container Registry, replace the login and push steps accordingly.
