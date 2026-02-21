# 🚀 FREE DEPLOYMENT GUIDE (Step-by-Step)

Since your project has two parts (Frontend & Backend), you need to deploy them to two different free services.

## 1️⃣ Part 1: Deploy Backend (Server) to RENDER
Render is the best place to host Node.js & Socket.io apps for free.

1.  **Create a GitHub Repository**:
    *   Initialize git in your project:
        ```bash
        cd C:\Users\joelm\.gemini\antigravity\scratch\hope-tutoring-centre
        git init
        git add .
        git commit -m "Initial commit"
        ```
    *   Create a repo on GitHub.com and push your code there.

2.  **Go to [Render.com](https://render.com)** and sign up.
3.  Click **"New +"** -> **"Web Service"**.
4.  Connect your GitHub repo.
5.  **Settings**:
    *   **Root Directory**: `server` (Important!)
    *   **Build Command**: `npm install`
    *   **Start Command**: `node index.js`
    *   **Instance Type**: Free
6.  Click **Deploy Web Service**.
7.  🚨 **COPY THE URL** Render gives you (e.g., `https://hope-server.onrender.com`). You need this next.

---

## 2️⃣ Part 2: Deploy Frontend (Client) to VERCEL
1.  Go to the client folder in your terminal:
    ```bash
    cd client
    ```
2.  Run the deploy command:
    ```bash
    npx vercel
    ```
3.  **Answer the questions**:
    *   Set up deploy? `y`
    *   Which scope? (Press Enter)
    *   Link to existing project? `N`
    *   Project name? `hope-tutoring-centre`
    *   Directory? `.` (or `./` - the default is fine)

4.  **🚨 IMPORTANT: Environment Variables**:
    *   When asked *"Want to modify these settings?"* -> Answer `y`
    *   Select **Environment Variables**.
    *   Add Variable Name: `VITE_SERVER_URL`
    *   Add Variable Value: `https://hope-server.onrender.com` (The URL you got from Render in Part 1)
    *   Add Variable Name: `VITE_SUPABASE_URL` 
    *   Value: (Your Supabase URL, or use placeholder if maintaining demo mode)
    *   Add Variable Name: `VITE_SUPABASE_ANON_KEY`
    *   Value: (Your Supabase Key)

    *(If you skip this, you can also set these in the Vercel Dashboard Settings later).*

5.  **Press Enter** to finish.
6.  Vercel will give you a final link: `https://hope-tutoring-centre.vercel.app`.

---

## 🎉 DONE!
*   **Frontend**: Hosted on Vercel (Fast CDN).
*   **Backend**: Hosted on Render (Real-time Sockets).
*   **Database**: Supabase (Cloud DB).

Your system is now live for the world!
