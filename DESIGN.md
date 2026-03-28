# AccidentAssist AI - Design System

This document outlines the **"Civic-Medical Authority"** design system for the **AccidentAssist AI** app, derived from Google Stitch designs.

## Creative North Star: "The Clinical Guardian"
In high-stress emergency scenarios, the UI functions as a calm, authoritative presence. It combines the reliability of a government institution with the precision of a modern surgical suite.

## 🎨 Color Palette
| Token | Hex Code | Purpose |
| :--- | :--- | :--- |
| **Primary** | `#006565` | Clinical Teal - signaling authority and professionalism. |
| **Emergency** | `#b62226` | Life-threatening action triggers (SOS). |
| **Base Surface** | `#f8f9fa` | Main background layer. |
| **Container Low** | `#f3f4f5` | Secondary content grouping. |
| **Container Lowest** | `#ffffff` | High-priority interactive cards. |
| **On Surface** | `#191c1d` | High-contrast text for critical readability. |

## 📐 Typography
- **Headlines & Instructions (Inter):** Bold weights for urgency.
- **Micro-copy & Technical Data (Public Sans):** Tabular feel to reinforce "Civic" authority.
- **Hierarchy:** Critical status updates must be scannable in under 2 seconds.

## 🧱 Component Structure
- **Emergency CTA (7rem height):** Large, thumb-targetable gradient button for 108 dispatch.
- **Reporting Grid:** Symmetrical cards for "Capture Scene" (Camera) and "Explain Situation" (Voice).
- **AI Clinical Guardian:** A "pulsing" container indicating real-time analysis status.
- **No-Line Rule:** Content sections are separated by tonal shifts (background color), not 1px solid borders.

## ♿ Accessibility Implementation
- **ARIA Roles:** All interactive cards use `role="button"` and `tabindex="0"`.
- **Descriptive Labels:** 
  - `SOS`: "Call Emergency Services Immediately"
  - `Upload`: "Upload Photo of Accident Scene"
  - `Record`: "Record Voice Report of Situation"
- **Color Contrast:** WCAG AA compliant on all critical text paths.
