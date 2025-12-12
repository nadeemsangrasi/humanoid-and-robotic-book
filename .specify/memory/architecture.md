# Architecture Document: Physical AI & Humanoid Robotics Textbook

## Overview

This document outlines the complete architecture of the Physical AI & Humanoid Robotics textbook project, including the frontend, backend, authentication, and deployment components.

## Architecture Components

### 1. Frontend Architecture

#### 1.1 Core Components
- **Framework**: Next.js 15 with React 19
- **UI Library**: OpenAI ChatKit React for chat interface
- **Authentication**: Better Auth for user authentication and session management
- **Styling**: Tailwind CSS with dark/light mode support
- **State Management**: React hooks and useChatKit from OpenAI ChatKit

#### 1.2 Authentication Layer
- **Better Auth Client**: Handles user authentication flow
- **Session Management**: Secure session tokens and user state
- **Protected Routes**: Authentication middleware for protected resources
- **User Profile**: Integration with Better Auth for user data access

#### 1.3 Database Integration
- **Drizzle ORM**: Type-safe database queries and schema management
- **PostgreSQL Neon DB**: Cloud-hosted PostgreSQL database with free tier support
- **Connection Pooling**: Efficient database connection management
- **Migrations**: Automated schema migrations using Drizzle Kit

### 2. Backend Architecture

#### 2.1 Core Services
- **Framework**: FastAPI with Uvicorn ASGI server
- **AI Integration**: OpenAI Agent SDK with Google Gemini models via compatibility layer
- **Vector Database**: Qdrant for book content embedding and retrieval
- **Embedding Service**: Google free embedding model via Langchain

#### 2.2 RAG System
- **Content Ingestion**: Scripts to process textbook content and create embeddings
- **Retrieval Pipeline**: Vector search and ranking of relevant content
- **Generation Engine**: Gemini models for answer synthesis
- **Response Formatting**: Clean, citation-friendly answers with source tracking

### 3. Authentication Architecture

#### 3.1 Frontend Authentication Flow
```
User -> Better Auth Client -> Session Token -> Protected Routes
     -> User Data -> Personalized Chat Experience
```

#### 3.2 Database Schema (Drizzle ORM)
- **Users Table**: User profiles, authentication data, preferences
- **Sessions Table**: Session tokens, expiration, user associations
- **Chat History Table**: User-specific chat history (optional)
- **Permissions Table**: User roles and access levels (if needed)

#### 3.3 Security Measures
- **Password Encryption**: Secure password hashing and storage
- **Session Security**: Secure, HttpOnly cookies for session management
- **Rate Limiting**: Protection against authentication abuse
- **CORS Configuration**: Secure cross-origin resource sharing

### 4. Database Architecture

#### 4.1 PostgreSQL Neon DB Configuration
- **Free Tier**: Utilizes Neon's free tier for cost-effective hosting
- **Branching**: Neon's branching feature for development/staging environments
- **Connection Pooling**: Optimized connection handling for performance
- **Backup Strategy**: Automated backups for data protection

#### 4.2 Drizzle ORM Setup
- **Schema Definition**: TypeScript-first schema definitions
- **Type Safety**: Full TypeScript support for database operations
- **Migrations**: Automated migration system for schema evolution
- **Query Builder**: Type-safe query building with SQL-like syntax

### 5. Integration Points

#### 5.1 Authentication & Chat Integration
- **User Context**: Authentication state passed to chat components
- **Personalization**: User-specific chat history and preferences
- **Access Control**: Authenticated users vs anonymous access
- **Rate Limiting**: Per-user rate limiting for API usage

#### 5.2 Frontend-Backend Communication
- **API Routes**: Next.js API routes for authentication endpoints
- **Database Actions**: Server actions for database operations
- **Session Validation**: Middleware for validating user sessions
- **Error Handling**: Consistent error handling across layers

### 6. Deployment Architecture

#### 6.1 Frontend Deployment
- **Static Hosting**: Next.js static export for Docusaurus integration
- **Authentication Endpoints**: API routes for auth functionality
- **Environment Configuration**: Secure environment variable management
- **CDN Integration**: Content delivery for optimal performance

#### 6.2 Backend Deployment
- **Docker Container**: Multi-stage Docker build for Hugging Face Spaces
- **Environment Variables**: Secure configuration management
- **Health Checks**: Application health monitoring
- **Logging**: Structured logging for debugging and monitoring

### 7. Security Considerations

#### 7.1 Data Protection
- **Encryption at Rest**: Database encryption for stored data
- **Encryption in Transit**: HTTPS for all communications
- **PII Handling**: Proper handling of personal information
- **Audit Logging**: Track authentication and data access events

#### 7.2 Access Control
- **Authentication**: Required for protected features
- **Authorization**: Role-based access control (if applicable)
- **Session Management**: Secure session handling and expiration
- **API Security**: Rate limiting and access validation

### 8. Performance Optimization

#### 8.1 Database Performance
- **Indexing Strategy**: Optimized database indexes for queries
- **Connection Pooling**: Efficient database connection management
- **Query Optimization**: Optimized queries for performance
- **Caching**: Strategic caching for frequently accessed data

#### 8.2 Frontend Performance
- **Bundle Optimization**: Optimized JavaScript bundle sizes
- **Code Splitting**: Dynamic imports for faster loading
- **Image Optimization**: Optimized image delivery
- **Caching Strategy**: Effective browser caching configuration

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Next.js 15, React 19 | User interface and application logic |
| Authentication | Better Auth | User authentication and session management |
| Database ORM | Drizzle ORM | Type-safe database operations |
| Database | PostgreSQL Neon DB | User data storage and management |
| Backend | FastAPI, Uvicorn | API server and business logic |
| AI/ML | Google Gemini via OpenAI SDK | RAG and content generation |
| Vector DB | Qdrant | Book content embedding and retrieval |
| Deployment | Docker, Hugging Face Spaces | Containerized deployment |
| Styling | Tailwind CSS | Responsive UI styling |

## Future Considerations

- **Scalability**: Horizontal scaling for increased user load
- **Monitoring**: Application performance monitoring and alerting
- **Analytics**: User engagement and usage analytics
- **Accessibility**: Enhanced accessibility compliance
- **Internationalization**: Multi-language support