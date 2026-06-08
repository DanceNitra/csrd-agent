# CSRD Agent

Multi-agent CSRD/ESRS compliance report generator.

## 🚀 Deploy na Render (Free Tier)

1. **Pushni repo** na GitHub (už hotové)

2. **Otvor** [dashboard.render.com](https://dashboard.render.com) → **New +** → **Web Service**

3. **Connect GitHub repo** `DanceNitra/csrd-agent`

4. **Nastav**:

   | Pole | Hodnota |
   |------|---------|
   | **Name** | `csrd-agent` |
   | **Runtime** | `Python 3` |
   | **Branch** | `main` |
   | **Region** | `Frankfurt (EU)` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn web.app:app --host 0.0.0.0 --port $PORT` |
   | **Instance Type** | **Free** ✓ |
   | **Health Check Path** | `/health` |

5. **Deploy** → počkaj 3-5 minút

6. **Otvoriť**: `https://csrd-agent.onrender.com`

7. **Overiť**: `https://csrd-agent.onrender.com/health`

## 🖥️ Lokálne spustenie

```bash
cd ~/csrd-agent
pip install -r requirements.txt
python3 web/app.py
# otvor http://localhost:8080
```

## 🏢 Pipeline

```bash
python3 cli.py --client Enel --full-pipeline --llm
```

## 📊 Reálni klienti

Enel, Volkswagen Group, Siemens, Iberdrola, TotalEnergies — 59 XBRL faktov.