act -j sast -W .github/workflows/test-sast-pipeline.yml
act -j zap_dast -W .github/workflows/test-dast-pipeline.yml