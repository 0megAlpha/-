s/((?:api[_-]?key|secret|token|passw(?:or)?d|credential)[A-Za-z0-9_]*["']?\s*[:=]\s*["']?)(?![\/.~\$])[A-Za-z0-9_+\/=-]{20,}/${1}REDACTED/gi;
