# Documentation Index

Complete documentation for the Bitcoin Macro Factor Dashboard.

---

## 📚 Quick Links

| Category | Document | Description |
|----------|----------|-------------|
| **Start Here** | [../README.md](../README.md) | Main project overview |
| **Setup** | [architecture/CLEAN_SETUP.md](architecture/CLEAN_SETUP.md) | Complete setup guide |
| **User Guide** | [user-guides/QUICK_START.md](user-guides/QUICK_START.md) | How to use the dashboard |

---

## 📁 Documentation Structure

```
docs/
├── INDEX.md                     ← You are here
│
├── architecture/                ← Code structure & implementation
│   ├── CLEAN_SETUP.md          ← Setup guide
│   ├── MODULAR_STRUCTURE.md    ← Component architecture
│   ├── MODULAR_QUICK_START.md  ← Quick reference
│   ├── IMPLEMENTATION_GUIDE.md ← Implementation details
│   └── CLEANUP_SUMMARY.md      ← Code cleanup history
│
├── data-updates/                ← Data freshness & updates
│   ├── DATA_FRESHNESS_README.md   ← Monitoring guide ⭐
│   ├── DATA_UPDATE_GUIDE.md       ← How updates work
│   └── REALTIME_OPTIONS_GUIDE.md  ← Real-time options
│
├── decisions/                   ← Design decisions
│   └── DECISION_LOG.md         ← Why current approach
│
└── user-guides/                 ← End-user documentation
    ├── QUICK_START.md          ← User guide
    └── UI_ENHANCEMENT_PREVIEW.md ← UI features preview
```

---

## 🎯 Find What You Need

### 🚀 Getting Started

**New to the project?**
1. [README.md](../README.md) - Project overview
2. [architecture/CLEAN_SETUP.md](architecture/CLEAN_SETUP.md) - Installation & setup
3. [user-guides/QUICK_START.md](user-guides/QUICK_START.md) - How to use

### 👨‍💻 For Developers

**Understanding the code:**
- [architecture/MODULAR_STRUCTURE.md](architecture/MODULAR_STRUCTURE.md) - Code organization
- [architecture/MODULAR_QUICK_START.md](architecture/MODULAR_QUICK_START.md) - Quick reference
- [architecture/IMPLEMENTATION_GUIDE.md](architecture/IMPLEMENTATION_GUIDE.md) - Implementation details

**Making changes:**
- [architecture/CLEAN_SETUP.md](architecture/CLEAN_SETUP.md) - Customization guide
- [architecture/CLEANUP_SUMMARY.md](architecture/CLEANUP_SUMMARY.md) - What changed

### 📊 About Data Updates

**Understanding data freshness:**
- [data-updates/DATA_FRESHNESS_README.md](data-updates/DATA_FRESHNESS_README.md) - How to monitor ⭐
- [data-updates/DATA_UPDATE_GUIDE.md](data-updates/DATA_UPDATE_GUIDE.md) - Detailed explanation

**Need more frequent updates?**
- [data-updates/REALTIME_OPTIONS_GUIDE.md](data-updates/REALTIME_OPTIONS_GUIDE.md) - All options explained
- [../future_implementations/](../future_implementations/) - Ready-to-deploy templates

### 🤔 Design Decisions

**Why was it built this way?**
- [decisions/DECISION_LOG.md](decisions/DECISION_LOG.md) - Rationale & alternatives

### 👥 For End Users

**Using the dashboard:**
- [user-guides/QUICK_START.md](user-guides/QUICK_START.md) - User guide
- [user-guides/UI_ENHANCEMENT_PREVIEW.md](user-guides/UI_ENHANCEMENT_PREVIEW.md) - Feature preview

---

## 📖 Documentation by Topic

### Architecture & Code Structure

| Document | What It Covers |
|----------|----------------|
| [MODULAR_STRUCTURE.md](architecture/MODULAR_STRUCTURE.md) | Complete component breakdown, file purposes, import guide |
| [MODULAR_QUICK_START.md](architecture/MODULAR_QUICK_START.md) | Quick reference for modular structure |
| [IMPLEMENTATION_GUIDE.md](architecture/IMPLEMENTATION_GUIDE.md) | Original implementation guide, feature details |
| [CLEAN_SETUP.md](architecture/CLEAN_SETUP.md) | Setup, configuration, customization |
| [CLEANUP_SUMMARY.md](architecture/CLEANUP_SUMMARY.md) | What changed in code cleanup |

### Data Updates & Freshness

| Document | What It Covers |
|----------|----------------|
| [DATA_FRESHNESS_README.md](data-updates/DATA_FRESHNESS_README.md) | How to monitor data freshness ⭐ |
| [DATA_UPDATE_GUIDE.md](data-updates/DATA_UPDATE_GUIDE.md) | How 24h cache works, FRED update frequencies |
| [REALTIME_OPTIONS_GUIDE.md](data-updates/REALTIME_OPTIONS_GUIDE.md) | Auto-refresh, polling, WebSocket options |

### Decisions & Rationale

| Document | What It Covers |
|----------|----------------|
| [DECISION_LOG.md](decisions/DECISION_LOG.md) | Why 24h cache, alternatives, when to change |

### User Guides

| Document | What It Covers |
|----------|----------------|
| [QUICK_START.md](user-guides/QUICK_START.md) | Dashboard tour, features, how to use |
| [UI_ENHANCEMENT_PREVIEW.md](user-guides/UI_ENHANCEMENT_PREVIEW.md) | UI improvements, feature preview |

---

## 🔍 Search by Question

### Setup & Installation

**Q: How do I install and run the dashboard?**
→ [architecture/CLEAN_SETUP.md](architecture/CLEAN_SETUP.md)

**Q: How do I configure indicators?**
→ [architecture/CLEAN_SETUP.md](architecture/CLEAN_SETUP.md#common-tasks)

**Q: How do I deploy to production?**
→ [../README.md](../README.md#deployment)

### Using the Dashboard

**Q: How do I use the dashboard?**
→ [user-guides/QUICK_START.md](user-guides/QUICK_START.md)

**Q: What features are available?**
→ [user-guides/UI_ENHANCEMENT_PREVIEW.md](user-guides/UI_ENHANCEMENT_PREVIEW.md)

**Q: How do I read the trading signals?**
→ [user-guides/QUICK_START.md](user-guides/QUICK_START.md#signals-dashboard)

### Data & Updates

**Q: How often does data update?**
→ [data-updates/DATA_FRESHNESS_README.md](data-updates/DATA_FRESHNESS_README.md)

**Q: Is the data real-time?**
→ [data-updates/DATA_UPDATE_GUIDE.md](data-updates/DATA_UPDATE_GUIDE.md)

**Q: Can I get more frequent updates?**
→ [data-updates/REALTIME_OPTIONS_GUIDE.md](data-updates/REALTIME_OPTIONS_GUIDE.md)

**Q: How do I check data freshness?**
→ [data-updates/DATA_FRESHNESS_README.md](data-updates/DATA_FRESHNESS_README.md#how-to-check)

### Development

**Q: How is the code organized?**
→ [architecture/MODULAR_STRUCTURE.md](architecture/MODULAR_STRUCTURE.md)

**Q: How do I add a new indicator?**
→ [architecture/CLEAN_SETUP.md](architecture/CLEAN_SETUP.md#add-new-indicator)

**Q: How do I modify components?**
→ [architecture/MODULAR_STRUCTURE.md](architecture/MODULAR_STRUCTURE.md#how-to-modify)

**Q: Where are reusable functions?**
→ [architecture/MODULAR_QUICK_START.md](architecture/MODULAR_QUICK_START.md#import-examples)

### Decisions & Why

**Q: Why 24-hour cache?**
→ [decisions/DECISION_LOG.md](decisions/DECISION_LOG.md)

**Q: What changed from original code?**
→ [architecture/CLEANUP_SUMMARY.md](architecture/CLEANUP_SUMMARY.md)

**Q: Why this architecture?**
→ [architecture/MODULAR_STRUCTURE.md](architecture/MODULAR_STRUCTURE.md#why-modular)

---

## ⭐ Most Important Docs

**Start with these:**

1. **[README.md](../README.md)** - Project overview, quick start
2. **[architecture/CLEAN_SETUP.md](architecture/CLEAN_SETUP.md)** - Complete setup guide
3. **[data-updates/DATA_FRESHNESS_README.md](data-updates/DATA_FRESHNESS_README.md)** - Data monitoring

**For development:**

4. **[architecture/MODULAR_STRUCTURE.md](architecture/MODULAR_STRUCTURE.md)** - Code structure
5. **[decisions/DECISION_LOG.md](decisions/DECISION_LOG.md)** - Design rationale

**For users:**

6. **[user-guides/QUICK_START.md](user-guides/QUICK_START.md)** - How to use the dashboard

---

## 📝 Contributing

When adding new documentation:

1. **Choose the right folder**:
   - Code/structure → `architecture/`
   - Data/updates → `data-updates/`
   - Decisions → `decisions/`
   - User-facing → `user-guides/`

2. **Update this INDEX.md** with the new document

3. **Update [README.md](../README.md)** if it's a major addition

4. **Use clear naming**: `WHAT_IT_COVERS.md` (ALL_CAPS for consistency)

---

## 🗂️ File Organization

**Root level** (project root):
- `README.md` - Main overview (stays at root for GitHub)
- `LICENSE` - License file
- `.env.example` - Environment template

**docs/** (this folder):
- All documentation except README.md
- Organized by category
- Easy to maintain and navigate

**future_implementations/**:
- Ready-to-deploy code templates
- Has its own README.md

---

## 🎯 Quick Navigation

| I Want To... | Go To... |
|--------------|----------|
| Install the dashboard | [architecture/CLEAN_SETUP.md](architecture/CLEAN_SETUP.md) |
| Learn to use it | [user-guides/QUICK_START.md](user-guides/QUICK_START.md) |
| Understand the code | [architecture/MODULAR_STRUCTURE.md](architecture/MODULAR_STRUCTURE.md) |
| Check data freshness | [data-updates/DATA_FRESHNESS_README.md](data-updates/DATA_FRESHNESS_README.md) |
| Enable real-time updates | [data-updates/REALTIME_OPTIONS_GUIDE.md](data-updates/REALTIME_OPTIONS_GUIDE.md) |
| Understand design choices | [decisions/DECISION_LOG.md](decisions/DECISION_LOG.md) |
| Customize indicators | [architecture/CLEAN_SETUP.md](architecture/CLEAN_SETUP.md#customization) |
| Deploy to production | [../README.md](../README.md#deployment) |

---

**All documentation is now organized and easy to find!** 📚
