# AGI Research Platform

> Một repo nghiên cứu quy mô lớn để mô phỏng hệ thống dữ liệu, kiến trúc nhận thức, huấn luyện liên tục, và hạ tầng train cho một **self-modeling intelligence platform**.

## Tuyên bố trung thực

Repo này **không tuyên bố tạo ra AGI có ý thức thật** hay “tự nhận thức” theo nghĩa triết học. Thay vào đó, nó cung cấp một nền tảng nghiên cứu có cấu trúc để thử nghiệm các năng lực gần với mục tiêu đó:

- world model + memory + planning
- self-model / self-reflection / calibration
- continual learning và curriculum adaptation
- cơ chế self-improvement có ràng buộc an toàn
- orchestration cho local / distributed training

Nói ngắn gọn: đây là một **research-grade scaffold** để phát triển một hệ thống thông minh đa thành phần, không chỉ là LLM wrapper.

## Kiến trúc tổng quan

```text
Data Generation / Curation
    -> Synthetic curricula, multi-domain tasks, reflection traces

Cognitive Core
    -> Episodic memory
    -> World model
    -> Self model
    -> Planner
    -> Governance / safety policy

Training System
    -> Adaptive curriculum
    -> Multi-objective optimization
    -> Self-improvement proposals
    -> Evaluation and reporting

Infrastructure
    -> Local launcher
    -> Distributed topology planning
    -> Docker + Compose + Kubernetes manifests
```

## Thư mục chính

- `src/agi_platform/data`: dữ liệu, schema, curriculum generation
- `src/agi_platform/cognition`: memory, self-model, world-model, planner, agent loop
- `src/agi_platform/training`: trainer, objectives, curriculum, self-improvement
- `src/agi_platform/infra`: launch plan cho local/distributed training
- `src/agi_platform/safety`: governance / safety constraints
- `configs`: cấu hình dữ liệu, model, train, infra
- `infra/k8s`: manifest để chạy job huấn luyện trên Kubernetes
- `tests`: smoke tests cho vòng lặp nhận thức và training
- `docs`: architecture và roadmap nghiên cứu

## Tính năng đã có

### 1. Data system
- Synthetic multi-domain task generator
- Structured `TaskSpec`, `Observation`, `Experience`
- Curriculum theo level và domain

### 2. Cognitive architecture
- `EpisodicMemory` để lưu kinh nghiệm
- `WorldModel` để ước lượng thành công theo domain
- `SelfModel` để tự đánh giá năng lực, calibration, priorities
- `Planner` để chọn chiến lược hành động theo reward / uncertainty / alignment
- `CognitiveAgent` để khép kín perception -> planning -> reflection -> memory

### 3. Training
- `AdaptiveCurriculum`
- Multi-objective scoring: reward, novelty, introspection, alignment
- `SelfImprovementEngine` đề xuất cập nhật nhỏ cho self-model
- `ResearchTrainer` để chạy nhiều episode, thu report

### 4. Infrastructure
- `TrainingTopology` mô tả node roles
- launcher plans cho local / Ray-like / Slurm-like workflows
- `Dockerfile`, `docker-compose.yml`, `infra/k8s/train-job.yaml`

## Chạy nhanh

### Windows CMD

```bat
set PYTHONPATH=src&& python -m agi_platform.main demo
```

### Kiểm tra smoke test

```bat
set PYTHONPATH=src&& python -m unittest discover -s tests -v
```

## Entry points

- `python -m agi_platform.main demo`
- `python -m agi_platform.main train --episodes 24`
- `python -m agi_platform.main architecture`
- `python -m agi_platform.main launch-plan --mode ray`

## Lộ trình tiếp theo

1. Thay synthetic generator bằng real multimodal pipelines
2. Thêm adapter cho PyTorch / JAX / DeepSpeed / Ray Train
3. Gắn tool use, retrieval, simulator environments
4. Bổ sung evaluator cho autonomy, robustness, calibration, long-horizon planning
5. Tách self-improvement thành sandboxed codegen + verifier loop

Xem thêm tại `docs/ARCHITECTURE.md` và `docs/ROADMAP.md`.