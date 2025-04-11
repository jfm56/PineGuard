declare namespace NodeJS {
  interface ProcessEnv {
    OPENAI_API_KEY: string;
    LLM_MODEL?: string;
    NODE_ENV: 'development' | 'production' | 'test';
  }
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}
