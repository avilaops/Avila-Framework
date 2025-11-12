# ============================================================================
# ARQUIVO DE CONFIGURAÇÃO - CONSOLIDAÇÃO DE DOCUMENTAÇÃO
# ============================================================================

@{
    # CONFIGURAÇÕES GERAIS
    DefaultOutputFileName = "RELATÓRIO_CORPORATIVO_CONSOLIDADO.md"
    CreateBackupByDefault = $true
    DeleteAnalyzedByDefault = $true
    BackupRetentionDays = 30
    
    # EXTENSÕES DE ARQUIVO SUPORTADAS
    SupportedExtensions = @(
        ".md", ".txt", ".json", ".yml", ".yaml",
        ".hpp", ".cpp", ".h", ".c",
        ".js", ".ts", ".jsx", ".tsx",
        ".py", ".rb", ".go", ".rs",
        ".ps1", ".sh", ".bat", ".cmd",
        ".sql", ".xml", ".csv",
        ".dockerfile", ".gitignore", ".env"
    )
    
    # ARQUIVOS PARA IGNORAR
    SkipPatterns = @(
        "RELATÓRIO_CORPORATIVO_CONSOLIDADO.md",
        "Consolidate-Documentation.ps1",
        "consolidation-config.ps1",
        "*.log", "*.tmp", "*.cache",
        "node_modules/*", ".git/*", "bin/*", "obj/*",
        "*.min.js", "*.min.css",
        "package-lock.json", "yarn.lock"
    )
    
    # REGRAS DE CATEGORIZAÇÃO
    CategoryRules = @{
        "Deployment & Infrastructure" = @{
            FilePatterns = @("*deploy*", "*migration*", "*infra*", "*docker*", "*k8s*", "*terraform*")
            ContentKeywords = @("deploy", "deployment", "migration", "database", "infrastructure", "terraform", "ansible", "docker", "kubernetes")
            Priority = 1
            Icon = "🚀"
        }
        
        "Artificial Intelligence & ML" = @{
            FilePatterns = @("*ai*", "*ml*", "*pipeline*", "*model*", "*training*")
            ContentKeywords = @("ai", "artificial intelligence", "machine learning", "llm", "gpt", "pipeline", "tensorflow", "pytorch", "model", "training")
            Priority = 1
            Icon = "🧠"
        }
        
        "Cloud & DevOps" = @{
            FilePatterns = @("*azure*", "*aws*", "*cloud*", "*devops*", "*ci*", "*cd*")
            ContentKeywords = @("azure", "aws", "cloud", "kubernetes", "docker", "devops", "ci/cd", "jenkins", "github actions")
            Priority = 1
            Icon = "☁️"
        }
        
        "Quality Assurance & Testing" = @{
            FilePatterns = @("*test*", "*qa*", "*quality*", "*spec*")
            ContentKeywords = @("codecov", "test", "testing", "quality", "ci/cd", "junit", "coverage", "automation")
            Priority = 2
            Icon = "✅"
        }
        
        "Security & Compliance" = @{
            FilePatterns = @("*security*", "*auth*", "*compliance*", "*audit*")
            ContentKeywords = @("security", "authentication", "authorization", "compliance", "audit", "oauth", "saml", "encryption")
            Priority = 2
            Icon = "🔒"
        }
        
        "Documentation & Guidelines" = @{
            FilePatterns = @("*instruction*", "*guide*", "*readme*", "*doc*", "*manual*")
            ContentKeywords = @("instruction", "guide", "how-to", "documentation", "manual", "readme", "guidelines")
            Priority = 2
            Icon = "📚"
        }
        
        "Database & Data Management" = @{
            FilePatterns = @("*database*", "*sql*", "*data*", "*schema*", "*migration*")
            ContentKeywords = @("database", "sql", "postgresql", "mysql", "mongodb", "schema", "data", "etl", "warehouse")
            Priority = 2
            Icon = "🗄️"
        }
        
        "Frontend Development" = @{
            FilePatterns = @("*ui*", "*frontend*", "*web*", "*react*", "*vue*", "*angular*")
            ContentKeywords = @("react", "vue", "angular", "frontend", "ui", "css", "html", "javascript", "typescript", "component")
            Priority = 3
            Icon = "🎨"
        }
        
        "Backend Development" = @{
            FilePatterns = @("*api*", "*backend*", "*server*", "*microservice*")
            ContentKeywords = @("api", "backend", "server", "microservice", "rest", "graphql", "endpoint", "service")
            Priority = 3
            Icon = "⚙️"
        }
        
        "C++ Development" = @{
            FilePatterns = @("*.cpp", "*.hpp", "*.h", "*.c")
            ContentKeywords = @("c++", "cpp", "header", "implementation", "algorithm", "performance")
            Priority = 3
            Icon = "⚡"
        }
        
        "JavaScript/TypeScript" = @{
            FilePatterns = @("*.js", "*.ts", "*.jsx", "*.tsx", "package.json")
            ContentKeywords = @("javascript", "typescript", "node", "npm", "yarn", "webpack", "babel")
            Priority = 3
            Icon = "📜"
        }
        
        "Configuration & Scripts" = @{
            FilePatterns = @("*.yml", "*.yaml", "*.json", "*.ps1", "*.sh", "*.bat", "*.env")
            ContentKeywords = @("configuration", "config", "script", "automation", "environment", "settings")
            Priority = 4
            Icon = "⚙️"
        }
        
        "General Documentation" = @{
            FilePatterns = @("*")
            ContentKeywords = @()
            Priority = 4
            Icon = "📄"
        }
    }
    
    # PALAVRAS-CHAVE PARA ANÁLISE
    TechnicalKeywords = @(
        # Tecnologias Cloud
        "Azure", "AWS", "GCP", "Kubernetes", "Docker", "Terraform", "Ansible",
        
        # Linguagens e Frameworks
        "JavaScript", "TypeScript", "React", "Vue", "Angular", "Node.js",
        "Python", "Django", "Flask", "C++", "Java", "Go", "Rust",
        
        # Bancos de Dados
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        
        # DevOps e CI/CD
        "Jenkins", "GitHub Actions", "GitLab CI", "CircleCI", "Codecov",
        "SonarQube", "Prometheus", "Grafana",
        
        # AI e ML
        "AI", "ML", "Machine Learning", "TensorFlow", "PyTorch", "OpenAI",
        "LangChain", "Embeddings", "Vector Database", "RAG",
        
        # Segurança
        "OAuth", "SAML", "JWT", "Security", "Authentication", "Authorization",
        
        # Arquitetura
        "Microservices", "API", "REST", "GraphQL", "Event-Driven", "CQRS",
        "Domain-Driven Design", "Clean Architecture"
    )
    
    # CONFIGURAÇÕES DE RELATÓRIO
    ReportSettings = @{
        IncludeFileMetrics = $true
        IncludeKeywordAnalysis = $true
        IncludeAutomaticSummary = $true
        MaxSummaryLength = 200
        TopKeywordsToShow = 10
        IncludeRecommendations = $true
        IncludeStatistics = $true
        DateFormat = "dd/MM/yyyy HH:mm:ss"
    }
    
    # CONFIGURAÇÕES DE BACKUP
    BackupSettings = @{
        CreateTimestampedBackups = $true
        CompressBackups = $false
        BackupLocation = ".\backups"
        MaxBackupCount = 10
    }
    
    # CONFIGURAÇÕES DE LOG
    LogSettings = @{
        EnableLogging = $true
        LogLevel = "Info" # Debug, Info, Warning, Error
        LogFile = "consolidation.log"
        MaxLogSize = "10MB"
    }
}