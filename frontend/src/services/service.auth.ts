import axios, { type AxiosResponse } from 'axios'
import type User from '@/model/User'
import type Token from '@/model/Token'

class AuthService {
  register(username: string, password: string): Promise<AxiosResponse<User>> {
    return axios.post<User>('/api/register', {
      username,
      password
    })
  }

  login(username: string, password: string): Promise<AxiosResponse<Token>> {
    return axios.post<Token>('/api/login', {
      username,
      password
    })
  }

  me(): Promise<AxiosResponse<User>> {
    return axios.get<User>('/api/me', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
  }
}

export default new AuthService()
