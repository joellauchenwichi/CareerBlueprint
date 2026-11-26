# CareerBlueprint
A career roadmap web app for students. Next.js frontend, FastAPI backend, with accounts and saved progress. AI-generated roadmaps coming next.

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

# Career Blueprint

A web app that turns a short survey into a step-by-step career roadmap for university students. Users create an account, answer questions about their goals and experience, and get a roadmap with tasks they can tick off. Their progress and notes are saved to their account.

## Status

Work in progress. The app works end to end, but the roadmap is currently generated from fixed rules, not AI. Making it smarter is the main thing we are working on next.

## What works now

- Sign up and log in with email and password
- A 7-step survey about goals, interests and experience
- A roadmap built from the survey answers, with tasks to check off
- Progress tracking, sticky notes, and a CV page
- Light and dark mode
- Progress saved to your account and available on any device

## Planned

- Generate roadmaps with an AI model instead of fixed rules (a backend endpoint for this already exists but is not connected to the frontend yet)
- Read an uploaded CV and use it to personalize the roadmap
- Deploy the app online

## Tech

- Frontend: Next.js (App Router), React, TypeScript, Tailwind CSS
- Backend: FastAPI (Python), SQLite
- Auth: email and password, salted password hashing, session tokens

## Run it locally

Backend:

    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

Frontend (in a second terminal):

    cd frontend
    npm install
    npm run dev

Then open http://localhost:3000.

To try the AI endpoint, copy `backend/.env.example` to `backend/.env` and add your own Nebius API key. The rest of the app works without it.

## Author

Joella, Computer Science and Hina, Computer and Social Science student at Minerva University
