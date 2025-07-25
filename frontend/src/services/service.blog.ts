import axios, { type AxiosResponse } from 'axios'
import type { Post, PostCreate, CommentCreate } from '@/model/Post'

interface UserStatistic {
  month: string
  user_count: number
}

interface StatisticsResponse<T> {
  title: string
  data: T[]
}

class BlogService {
  // Posts abrufen
  getPosts(skip: number = 0, limit: number = 10): Promise<AxiosResponse<Post[]>> {
    return axios.get<Post[]>(`/api/posts?skip=${skip}&limit=${limit}`)
  }

  // Einzelnen Post abrufen
  getPost(postId: string): Promise<AxiosResponse<Post>> {
    return axios.get<Post>(`/api/posts/${postId}`)
  }

  // Neuen Post erstellen
  createPost(postData: PostCreate): Promise<AxiosResponse<Post>> {
    return axios.post<Post>('/api/posts', postData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
  }

  // Kommentar hinzufügen
  addComment(postId: string, commentData: CommentCreate): Promise<AxiosResponse<{ message: string }>> {
    return axios.post<{ message: string }>(`/api/posts/${postId}/comments`, commentData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
  }

  // Posts eines bestimmten Users
  getUserPosts(userId: string): Promise<AxiosResponse<Post[]>> {
    return axios.get<Post[]>(`/api/users/${userId}/posts`)
  }

  // Statistiken - Nutzer pro Monat
  getUsersByMonth(): Promise<AxiosResponse<StatisticsResponse<UserStatistic>>> {
    return axios.get<StatisticsResponse<UserStatistic>>('/api/stats/users-by-month')
  }
}

export default new BlogService()
