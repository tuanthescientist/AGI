# Architecture

## 1. Why this repo exists

Nếu chỉ fine-tune một LLM, ta thường nhận được một hệ thống mạnh về text completion nhưng yếu ở:

- self-calibration
- long-horizon agency
- structured memory
- adaptive curriculum
- introspective correction
- safe self-modification

Repo này mô hình hóa AGI như một hệ nhiều vòng lặp:

1. **Perceive**: tiếp nhận task / observation
2. **Model**: cập nhật world model và self model
3. **Plan**: chọn hành động có utility cao
4. **Act**: thực thi chiến lược
5. **Reflect**: đánh giá reward, uncertainty, alignment
6. **Improve**: đề xuất self-modification nhỏ, có giới hạn

## 2. Core abstractions

### TaskSpec
- domain
- difficulty
- target skill
- success criteria

### Experience
- observation
- action
- reward
- uncertainty
- alignment score
- introspection note

### SelfModel
- capability scores theo domain
- calibration
- priorities cho improvement

### WorldModel
- success priors theo domain và strategy
- uncertainty estimate

### GovernancePolicy
- chặn các update quá lớn
- bảo toàn ràng buộc an toàn

## 3. Research extension points

- thay synthetic task bằng benchmark thật
- thêm module model backend cho transformers
- thêm replay buffer, retrieval memory, tool use
- thêm automatic evaluator và judge models
- thêm sandbox cho code self-improvement