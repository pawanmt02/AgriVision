# 🚀 Deploying AgriVision to Vercel

AgriVision is pre-configured for seamless, zero-config deployment on [Vercel](https://vercel.com).

---

## ⚡ Option 1: Deploy with Git (Recommended)

1. **Push your code to GitHub / GitLab / Bitbucket**:
   ```bash
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

2. **Import into Vercel Dashboard**:
   - Go to [vercel.com/new](https://vercel.com/new).
   - Select your **AgriVision** repository.
   - **Framework Preset**: Select **Next.js**.
   - **Root Directory**:
     - If you want Vercel to build the root repo directly, keep `./` (the root `vercel.json` will automatically build `frontend/`).
     - Or click **Edit** and set Root Directory to `frontend`.
   - Click **Deploy**!

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
