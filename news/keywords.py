"""
智能关键词扩展系统
根据用户输入的关键词，自动扩展相关领域的技术术语
"""
import re
from typing import Dict, List, Optional
from logger import get_logger

class KeywordExpander:
    """关键词扩展器"""

    def __init__(self):
        self.logger = get_logger()

        # 预定义的领域关键词映射
        self.domain_keywords: Dict[str, List[str]] = {
            # AI & LLM 领域
            "ai": [
                "AI", "LLM", "GPT", "Claude", "Generative", "Machine Learning",
                "Deep Learning", "Neural Network", "NLP", "Transformer",
                "Diffusion", "Stable Diffusion", "Midjourney", "ChatGPT",
                "OpenAI", "Anthropic", "LangChain", "RAG", "Agent", "Copilot",
                "Sora", "Gemini", "Llama", "Mistral", "Embedding", "Fine-tuning"
            ],
            "llm": [
                "LLM", "GPT", "Claude", "ChatGPT", "Llama", "Gemini", "Mistral",
                "LangChain", "RAG", "Prompt", "Token", "Context", "Inference",
                "Fine-tuning", "LoRA", "QLoRA", "Embedding", "Vector DB"
            ],
            "deepseek": [
                "DeepSeek", "deepseek", "V3", "R1", "Janus", "DeepSeek-R1"
            ],

            # 开发与编程
            "android": [
                "Android", "Kotlin", "Jetpack Compose", "Flutter", "React Native",
                "Mobile", "Gradle", "SDK", "APK", "AAB"
            ],
            "web": [
                "JavaScript", "TypeScript", "React", "Vue", "Angular", "Next.js",
                "Nuxt", "Svelte", "Frontend", "WebAssembly", "Vite", "Webpack"
            ],
            "backend": [
                "Backend", "API", "REST", "GraphQL", "gRPC", "Microservices",
                "Docker", "Kubernetes", "Serverless", "Edge Computing"
            ],
            "python": [
                "Python", "Django", "Flask", "FastAPI", "PyTorch", "TensorFlow",
                "Pandas", "NumPy", "Asyncio", "Poetry", "uv"
            ],
            "rust": [
                "Rust", "Cargo", "Tokio", "wasm", "memory safety", "systems programming"
            ],
            "go": [
                "Go", "Golang", "goroutine", "channel", "Gin", "Echo", "microservices"
            ],

            # 云与基础设施
            "cloud": [
                "Cloud", "AWS", "Azure", "GCP", "Serverless", "Lambda",
                "EC2", "S3", "Docker", "Kubernetes", "Terraform", "Infrastructure"
            ],
            "devops": [
                "DevOps", "CI/CD", "GitHub Actions", "GitLab", "Jenkins",
                "ArgoCD", "Monitoring", "Observability", "Prometheus", "Grafana"
            ],

            # 数据与数据库
            "database": [
                "Database", "SQL", "NoSQL", "PostgreSQL", "MySQL", "MongoDB",
                "Redis", "SQLite", "DynamoDB", "Cassandra", "TimescaleDB"
            ],
            "data": [
                "Data", "Analytics", "Big Data", "Data Lake", "Warehouse",
                "ETL", "Pipeline", "Streaming", "Kafka", "Snowflake", "Databricks"
            ],

            # 安全领域
            "security": [
                "Security", "Cybersecurity", "Encryption", "Zero Trust",
                "Authentication", "OAuth", "JWT", "Firewall", "Penetration Testing"
            ],

            # 金融与商业
            "finance": [
                "Finance", "FinTech", "Trading", "Stock", "Crypto", "Bitcoin",
                "Ethereum", "Blockchain", "DeFi", "Payment", "Banking"
            ],
            "crypto": [
                "Crypto", "Bitcoin", "Ethereum", "DeFi", "NFT", "Web3",
                "Blockchain", "Smart Contract", "Solana", "Polygon"
            ],

            # 产品与设计
            "product": [
                "Product", "SaaS", "B2B", "B2C", "UX", "UI", "Design",
                "Product Management", "Roadmap", "MVP", "PMF"
            ],

            # 创投与商业
            "startup": [
                "Startup", "Venture Capital", "VC", "Funding", "Series A",
                "IPO", "Unicorn", "Pitch Deck", "Accelerator", "Y Combinator"
            ],

            # 开源
            "open source": [
                "Open Source", "OSS", "GitHub", "Git", "License", "MIT",
                "Apache", "GPL", "Community", "Contribution"
            ],
        }

    def expand(self, keyword: str) -> str:
        """
        扩展关键词

        Args:
            keyword: 用户输入的关键词（可以是逗号分隔的多个关键词）

        Returns:
            扩展后的逗号分隔关键词字符串
        """
        if not keyword:
            return ""

        # 解析用户输入的关键词
        user_keywords = [k.strip().lower() for k in keyword.split(',') if k.strip()]

        expanded_keywords = set(user_keywords)

        for kw in user_keywords:
            # 检查是否匹配预定义领域
            for domain, terms in self.domain_keywords.items():
                if kw in domain.lower() or domain.lower() in kw:
                    # 添加该领域的所有相关术语
                    expanded_keywords.update(terms)
                    self.logger.info(f"关键词 '{kw}' 扩展到领域 '{domain}'，添加 {len(terms)} 个术语")

        # 返回逗号分隔的字符串
        result = ",".join(sorted(expanded_keywords))
        self.logger.info(f"关键词扩展: '{keyword}' -> '{result}'")
        return result

    def get_domain_keywords(self, domain: str) -> List[str]:
        """获取特定领域的所有关键词"""
        domain_lower = domain.lower()
        for key, keywords in self.domain_keywords.items():
            if domain_lower in key or key in domain_lower:
                return keywords
        return []

    def add_custom_domain(self, domain: str, keywords: List[str]):
        """添加自定义领域关键词"""
        self.domain_keywords[domain.lower()] = keywords
        self.logger.info(f"添加自定义领域 '{domain}' 包含 {len(keywords)} 个关键词")


# 全局实例
_expander = None

def get_expander() -> KeywordExpander:
    """获取关键词扩展器实例"""
    global _expander
    if _expander is None:
        _expander = KeywordExpander()
    return _expander
