import { useMutation, useQuery } from "@tanstack/react-query";
import { api } from "./base"
import type { ColumnDef } from "@tanstack/react-table";

interface VideoFile {
  content: string;
  start: string;
  end: string;
  id: string

}


export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await api.post('/videos/embed', formData);
  return res;
}

export const useUploadFile = () => {
  return useMutation({
    mutationKey: ['video', 'upload'],
    mutationFn: (file: File) => uploadFile(file)
  })
}

export const getFilesByQuery = async (query: string, k?: number): Promise<VideoFile[]> => {
  const res = await api.post('/videos/search', {
    query: query,
    k: 5
  },{
   headers: {
        "Content-Type": "application/json",
      }
    },)
  return res.data;
}

export const useGetFilesByQuery = (query: string, k?: number) => {
  return useMutation({
    mutationKey: ['video', 'query'],
    mutationFn: () => 
      getFilesByQuery(query, k),
  })
}

export const getAllFiles = async (): Promise<VideoFile[]> => {
   const res = await api.get('/videos/all');
   return res.data;
}

export const useGetAllFiles = () => {
  return useQuery({
    queryKey: ['video', 'all'],
    queryFn: () => getAllFiles()
  })
}


export const columns: ColumnDef<VideoFile>[] = [
  {
    accessorKey: "id",
    header: "id",
  },
  {
    accessorKey: "content",
    header: "Content",
  },
  {
    accessorKey: "start",
    header: "Start",
  },
  {
    accessorKey: "end",
    header: "End",
  },
]