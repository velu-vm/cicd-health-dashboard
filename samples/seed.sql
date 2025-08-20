-- Seed data for CI/CD Health Dashboard
-- This file contains sample data for development and testing

-- Insert sample pipelines
INSERT INTO pipelines (name, repository, owner, branch, workflow_file, status, last_run_number, last_run_url, last_run_time, created_at, updated_at) VALUES
('Frontend CI/CD', 'frontend-app', 'myorg', 'main', '.github/workflows/frontend.yml', 'success', 42, 'https://github.com/myorg/frontend-app/actions/runs/42', NOW() - INTERVAL '1 hour', NOW(), NOW()),
('Backend API', 'backend-api', 'myorg', 'main', '.github/workflows/backend.yml', 'success', 156, 'https://github.com/myorg/backend-api/actions/runs/156', NOW() - INTERVAL '30 minutes', NOW(), NOW()),
('Mobile App', 'mobile-app', 'myorg', 'develop', '.github/workflows/mobile.yml', 'running', 89, 'https://github.com/myorg/mobile-app/actions/runs/89', NOW() - INTERVAL '15 minutes', NOW(), NOW()),
('Infrastructure', 'infra-as-code', 'myorg', 'main', '.github/workflows/terraform.yml', 'failed', 23, 'https://github.com/myorg/infra-as-code/actions/runs/23', NOW() - INTERVAL '2 hours', NOW(), NOW());

-- Insert sample workflow runs
INSERT INTO workflow_runs (pipeline_id, run_number, run_id, status, conclusion, start_time, end_time, duration, commit_hash, commit_message, author, run_url, workflow_name, trigger, metadata, created_at) VALUES
(1, 42, '123456789', 'success', 'success', NOW() - INTERVAL '1 hour 5 minutes', NOW() - INTERVAL '1 hour', 300, 'abc123def456', 'feat: add new dashboard component', 'john.doe', 'https://github.com/myorg/frontend-app/actions/runs/42', 'Frontend CI/CD', 'push', '{"actor": "john.doe", "head_branch": "main"}', NOW()),
(1, 41, '123456788', 'success', 'success', NOW() - INTERVAL '2 hours 5 minutes', NOW() - INTERVAL '2 hours', 280, 'def456ghi789', 'fix: resolve styling issues', 'jane.smith', 'https://github.com/myorg/frontend-app/actions/runs/41', 'Frontend CI/CD', 'push', '{"actor": "jane.smith", "head_branch": "main"}', NOW()),
(2, 156, '987654321', 'success', 'success', NOW() - INTERVAL '30 minutes 3 minutes', NOW() - INTERVAL '30 minutes', 180, 'ghi789jkl012', 'feat: add new API endpoint', 'bob.wilson', 'https://github.com/myorg/backend-api/actions/runs/156', 'Backend API', 'pull_request', '{"actor": "bob.wilson", "head_branch": "feature/new-endpoint"}', NOW()),
(3, 89, '456789123', 'running', NULL, NOW() - INTERVAL '15 minutes', NULL, NULL, 'jkl012mno345', 'feat: implement push notifications', 'alice.johnson', 'https://github.com/myorg/mobile-app/actions/runs/89', 'Mobile App', 'push', '{"actor": "alice.johnson", "head_branch": "develop"}', NOW()),
(4, 23, '789123456', 'failed', 'failure', NOW() - INTERVAL '2 hours 10 minutes', NOW() - INTERVAL '2 hours', 600, 'mno345pqr678', 'feat: add new cloud resources', 'charlie.brown', 'https://github.com/myorg/infra-as-code/actions/runs/23', 'Infrastructure', 'push', '{"actor": "charlie.brown", "head_branch": "main"}', NOW());

-- Insert sample alerts
INSERT INTO alerts (pipeline_id, type, message, severity, is_active, created_at) VALUES
(4, 'workflow_failed', 'Infrastructure pipeline failed on commit mno345pqr678', 'high', true, NOW() - INTERVAL '2 hours'),
(3, 'workflow_slow', 'Mobile app pipeline has been running for over 15 minutes', 'medium', true, NOW() - INTERVAL '5 minutes'),
(1, 'workflow_success', 'Frontend pipeline completed successfully', 'low', false, NOW() - INTERVAL '1 hour');

-- Update pipeline status based on latest runs
UPDATE pipelines SET 
    status = 'success',
    last_run_number = 42,
    last_run_url = 'https://github.com/myorg/frontend-app/actions/runs/42',
    last_run_time = NOW() - INTERVAL '1 hour',
    updated_at = NOW()
WHERE id = 1;

UPDATE pipelines SET 
    status = 'success',
    last_run_number = 156,
    last_run_url = 'https://github.com/myorg/backend-api/actions/runs/156',
    last_run_time = NOW() - INTERVAL '30 minutes',
    updated_at = NOW()
WHERE id = 2;

UPDATE pipelines SET 
    status = 'running',
    last_run_number = 89,
    last_run_url = 'https://github.com/myorg/mobile-app/actions/runs/89',
    last_run_time = NOW() - INTERVAL '15 minutes',
    updated_at = NOW()
WHERE id = 3;

UPDATE pipelines SET 
    status = 'failed',
    last_run_number = 23,
    last_run_url = 'https://github.com/myorg/infra-as-code/actions/runs/23',
    last_run_time = NOW() - INTERVAL '2 hours',
    updated_at = NOW()
WHERE id = 4;
