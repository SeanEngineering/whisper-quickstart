import { api } from "./base"

export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await api.post('/videos/embed', formData);
  return res;
}