# Skill IR（语义契约）规范

## 定义

Skill IR 是技能的机器可读语义契约，描述技能"做什么"、"要什么"、"给什么"。

## 格式（YAML）

```yaml
skill_ir:
  name: "技能名"
  version: "1.0.0"
  intent: "一句话描述核心意图"
  triggers:
    - "关键词1"
    - "关键词2"
  inputs:
    - name: "输入名"
      type: "text|file|url|path"
      required: true
      description: "描述"
  outputs:
    - name: "输出名"
      type: "text|file|json"
      description: "描述"
  dependencies:
    tools: ["Read", "Write", "Bash"]
    skills: ["urlgo"]  # 依赖的其他技能
    env: ["API_KEY"]    # 环境变量
  quality_gates:
    min_signal_density: 0.8
    max_tokens: 300
    required_sections: ["Keywords", "Summary", "Strategy", "AVOID"]
```

## 用途

- 创建技能时自动生成 IR
- 诊断时用 IR 做结构化验证
- 发布时 IR 作为元数据上传

## 生成流程

1. 从需求中提取信息
2. 填充 IR 字段
3. 验证 IR 完整性
4. 保存为 `skill-ir.json`

## 验证规则

- name：必须存在，非空
- version：必须符合语义化版本格式
- triggers：至少一个触发词
- inputs：可选，但若存在则必须有 name 和 type
- outputs：可选，但若存在则必须有 name 和 type
- quality_gates：必须包含 min_signal_density 和 max_tokens

## AVOID

- AVOID IR 字段缺失
- AVOID 版本号格式错误
- AVOID 触发词为空
- AVOID 质量门禁阈值不合理
