export type ApiApp = {
  name: string;
  description: string;
  type: string;
  app_id: string;
  approval_github_url?: string;
  clear_state_github_url?: string;
  github_url?: string;
};

export type AppType = {
  key: number;
  name: string;
  description: string;
  appType: string;
  appId: string;
  githubUrl: (string | undefined)[];
};

export type VerifyTealAppPayload = {
  app_id?: string;
  name?: string;
  description?: string;
  approval_github_url?: string;
  clear_state_github_url?: string;
};

export type FormState = {
  appId?: string;
  name?: string;
  description?: string;
  type?: string;
  githubUrl?: string;
  approvalUrl?: string;
  clearStateUrl?: string;
};
