export interface Comment {
  text: string
  author_id: string
  author_username: string
  created_at: string
}

export interface Post {
  id: string
  title: string
  content: string
  author_id: string
  author_username: string
  created_at: string
  comments: Comment[]
}

export interface PostCreate {
  title: string
  content: string
}

export interface CommentCreate {
  text: string
}
