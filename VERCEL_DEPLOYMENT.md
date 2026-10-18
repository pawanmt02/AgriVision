# 🚀 Deploying AgriVision to Vercel

AgriVision is pre-configured for seamless, zero-config deployment on [Vercel](https://vercel.com).

---

## ⚡ How to Fix the 404 & Deploy Cleanly

### 1. In your Vercel Dashboard (Currently open in your browser)
1. In the **agrivision1** project, click the **Settings** tab at the top.
2. Under **General**, find **Root Directory**.
3. Click **Edit**, type or select:
   ```
   frontend
   ```
4. Click **Save**.

### 2. Redeploy
1. Click the **Deployments** tab at the top.
2. Click the three dots (`...`) next to the latest deployment.
3. Click **Redeploy** (you can leave "Use existing build cache" unchecked).
4. Once completed, your app will be live at `https://agrivision1-six.vercel.app/` without any 404 errors!

---

## 💻 Option 2: Deploy using Vercel CLI

```bash
# 1. Install Vercel CLI (if not already installed)
npm install -g vercel

# 2. Deploy from the project root
vercel

# 3. For Production release
vercel --prod
```

---

## 🌐 Dual Architecture: Standalone vs Full Backend

### Mode A: Standalone Vercel Serverless (Default)
Out-of-the-box, the Vercel deployment includes full Next.js Serverless Edge API routes under `/api/*`:
- `/api/health`: Health status & version check
- `/api/diagnose`: Real-time image diagnostic engine (identifies crop diseases, detects animals & food, generates organic & chemical prescriptions)
- `/api/outbreaks`: Geospatial disease outbreak cluster mapping
- `/api/analytics`: Outbreak metrics and crop severity breakdowns
- `/api/sample-images`: Interactive test leaf gallery

**Zero configuration required!**

---

### Mode B: Connected to Python FastAPI Core
If you host the Python PyTorch core (`backend/main.py`) on **Render**, **Railway**, or **Hugging Face Spaces**:
1. Open your project settings in the **Vercel Dashboard**.
2. Navigate to **Settings** > **Environment Variables**.
3. Add the variable:
   - **Key**: `NEXT_PUBLIC_BACKEND_URL`
   - **Value**: `https://your-backend-api.onrender.com` (your deployed backend URL)
4. Redeploy. AgriVision will automatically proxy all deep neural inference and SQLite spatial queries directly to your dedicated Python core!
