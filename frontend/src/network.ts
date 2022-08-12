import { BACKEND_BASE_URL } from "./constants";
import axios from "axios";
import { ApiApp, VerifyTealAppPayload } from "./types";

const api = axios.create({
  baseURL: `${BACKEND_BASE_URL}/apps`,
});

export const getVerifiedApps = async (): Promise<ApiApp[]> => {
  const response = await api.get("");
  return response.data.apps;
};

export const verifyTealApp = async (payload: VerifyTealAppPayload) => {
  const response = await api.post("/teal/verify/", payload);
  return response.data;
};
