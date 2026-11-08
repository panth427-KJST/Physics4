"""make_art.py — สร้างภาพประกอบ SVG ของแต่ละบทจากการคำนวณจริง แล้วแทรกลงใน index.html
ใช้: python3 tools/make_art.py   (แทนที่ <!--ART:key--> ... <!--/ART--> ใน index.html)
"""
import math, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEEP = '#0B1F3A'; OCEAN = '#123A63'; WAVE = '#1E6091'; CREST = '#3BA3C7'; FOAM = '#7FD8E8'
SUN = '#F4B740'; CORAL = '#E8654A'; OK = '#12B886'; VIOLET = '#B49BFF'

def poly(pts): return 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
def frange(a, b, s):
    out, x = [], a
    while x <= b + 1e-9: out.append(x); x += s
    return out
def wrap(body, extra_defs=''):
    return ('<svg viewBox="0 0 400 240" xmlns="http://www.w3.org/2000/svg" role="img" '
            'preserveAspectRatio="xMidYMid slice" stroke-linecap="round" stroke-linejoin="round">'
            '<defs>%s</defs>%s</svg>') % (extra_defs, body)

# ---------------------------------------------------------------- บทที่ 12 เสียง
def art_sound():
    g = '<linearGradient id="bg12" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0E2A4D"/><stop offset="1" stop-color="#0B1F3A"/></linearGradient>'
    b = ['<rect width="400" height="240" fill="url(#bg12)"/>']
    # อนุภาคอากาศ: ตำแหน่งสมดุลเป็นกริด เลื่อนตาม s = A sin(kx) → ส่วนอัด/ส่วนขยายจริง
    lam, A, x0 = 104, 15, 70
    k = 2 * math.pi / lam
    for row in range(7):
        y = 58 + row * 19
        for i in range(44):
            xe = x0 + i * 8 + (row % 2) * 4
            if xe > 410: break
            xs = xe + A * math.sin(k * (xe - x0) - math.pi / 2)
            b.append('<circle cx="%.1f" cy="%.1f" r="2.4" fill="#CDEFF6" opacity=".85"/>' % (xs, y))
    # กราฟความดัน Δp (เฟสต่างจากการกระจัด 90°) แถบล่าง
    y0 = 222
    b.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.6"/>' % (poly([(x, y0 - 12 * math.cos(k * (x - x0) - math.pi / 2)) for x in frange(x0, 400, 2)]), SUN))
    # ลำโพงด้านซ้าย
    b.append('<path d="M14 104 h16 l24 -24 v80 l-24 -24 h-16 z" fill="%s" stroke="%s" stroke-width="2.4"/>' % (OCEAN, FOAM))
    for r in (20, 34):
        b.append('<path d="M%d %d a%d %d 0 0 1 0 %d" fill="none" stroke="%s" stroke-width="2" opacity=".8"/>' % (58 + r * 0.2, 120 - r, r, r, 2 * r, CORAL))
    # วงเล็บ λ ระหว่างส่วนอัด 2 แห่ง (ส่วนอัดอยู่ที่ k(x-x0)-π/2 = π/2 + 2πn → x = x0 + λ/2 + nλ)
    c1 = x0 + lam / 2 + lam; c2 = c1 + lam; yb = 196
    b.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.6"/>' % (c1, yb, c2, yb, SUN))
    for xx in (c1, c2):
        b.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.6"/>' % (xx, yb - 5, xx, yb + 5, SUN))
    b.append('<text x="%.1f" y="%d" fill="%s" font-family="Prompt, sans-serif" font-weight="700" font-size="16" text-anchor="middle">λ</text>' % ((c1 + c2) / 2 + 12, yb + 5, SUN))
    b[-1] = b[-1].replace('text-anchor="middle"', 'text-anchor="start"').replace('x="%.1f"' % ((c1 + c2) / 2 + 12), 'x="%.1f"' % (c2 + 8))
    return wrap(''.join(b), g)

# ---------------------------------------------------------------- บทที่ 13 ไฟฟ้าสถิต (เส้นสนามของประจุคู่)
def art_electrostatics():
    g = ('<linearGradient id="bg13" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22184A"/><stop offset="1" stop-color="#0B1F3A"/></linearGradient>'
         '<radialGradient id="qp"><stop offset="0" stop-color="#FFD6CC"/><stop offset="1" stop-color="%s"/></radialGradient>'
         '<radialGradient id="qn"><stop offset="0" stop-color="#D6F4FA"/><stop offset="1" stop-color="%s"/></radialGradient>') % (CORAL, CREST)
    b = ['<rect width="400" height="240" fill="url(#bg13)"/>']
    P, N = (130, 120), (270, 120)
    def E(x, y):
        ex = ey = 0.0
        for (qx, qy), q in ((P, 1), (N, -1)):
            dx, dy = x - qx, y - qy; r3 = (dx * dx + dy * dy) ** 1.5 + 1e-9
            ex += q * dx / r3; ey += q * dy / r3
        return ex, ey
    n = 16
    for i in range(n):
        a = 2 * math.pi * (i + 0.5) / n
        x, y = P[0] + 10 * math.cos(a), P[1] + 10 * math.sin(a)
        pts = [(x, y)]
        for _ in range(900):
            ex, ey = E(x, y); m = math.hypot(ex, ey)
            x += 1.5 * ex / m; y += 1.5 * ey / m
            pts.append((x, y))
            if math.hypot(x - N[0], y - N[1]) < 10 or not (-40 < x < 440 and -40 < y < 280): break
        b.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.6" opacity=".75"/>' % (poly(pts), VIOLET))
        # หัวลูกศรกลางเส้น (ทิศของ E ออกจาก + เข้า −)
        j = len(pts) // 2
        (x1, y1), (x2, y2) = pts[j - 1], pts[j + 1]
        ang = math.atan2(y2 - y1, x2 - x1); xm, ym = pts[j]
        tip = (xm + 5 * math.cos(ang), ym + 5 * math.sin(ang))
        l = (xm - 4 * math.cos(ang) + 3.5 * math.sin(ang), ym - 4 * math.sin(ang) - 3.5 * math.cos(ang))
        r = (xm - 4 * math.cos(ang) - 3.5 * math.sin(ang), ym - 4 * math.sin(ang) + 3.5 * math.cos(ang))
        b.append('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f z" fill="%s" opacity=".9"/>' % (tip + l + r + (VIOLET,)))
    for (qx, qy), grad, s in ((P, 'qp', '+'), (N, 'qn', '−')):
        b.append('<circle cx="%d" cy="%d" r="15" fill="url(#%s)"/>' % (qx, qy, grad))
        b.append('<text x="%d" y="%d" fill="%s" font-family="Prompt, sans-serif" font-weight="800" font-size="20" text-anchor="middle">%s</text>' % (qx, qy + 7, DEEP, s))
    return wrap(''.join(b), g)

# ---------------------------------------------------------------- บทที่ 14 ไฟฟ้ากระแส (วงจรอนุกรม)
def art_current():
    g = '<linearGradient id="bg14" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3A2A10"/><stop offset="1" stop-color="#0B1F3A"/></linearGradient>'
    b = ['<rect width="400" height="240" fill="url(#bg14)"/>']
    L, R, T, B = 70, 330, 60, 190
    b.append('<path d="M%d %d H%d V%d H%d Z" fill="none" stroke="%s" stroke-width="3"/>' % (L, T, R, B, L, '#E8D9B8'))
    # แบตเตอรี่ (ด้านซ้าย) — เส้นยาว = ขั้วบวก
    yc = (T + B) / 2
    b.append('<rect x="%d" y="%d" width="22" height="34" fill="#2A1E0C"/>' % (L - 11, yc - 17))
    b.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (L - 16, yc - 7, L + 16, yc - 7, SUN))
    b.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="5"/>' % (L - 9, yc + 7, L + 9, yc + 7, SUN))
    # ตัวต้านทานสองตัว (ซิกแซก) ด้านบน
    for x0 in (135, 225):
        pts = [(x0, T)] + [(x0 + 6 + 8 * i, T + (-9 if i % 2 == 0 else 9)) for i in range(5)] + [(x0 + 46, T)]
        b.append('<rect x="%d" y="%d" width="46" height="24" fill="#2A1E0C"/>' % (x0, T - 12))
        b.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.6"/>' % (poly(pts), CORAL))
    # หลอดไฟด้านขวา
    b.append('<circle cx="%d" cy="%d" r="16" fill="#2A1E0C" stroke="%s" stroke-width="2.6"/>' % (R, yc, SUN))
    b.append('<path d="M%d %d l8 8 M%d %d l-8 8" stroke="%s" stroke-width="2"/>' % (R - 4, yc - 4, R + 4, yc - 4, SUN))
    for a in range(0, 360, 45):
        ra = math.radians(a)
        b.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6" opacity=".55"/>' % (R + 22 * math.cos(ra), yc + 22 * math.sin(ra), R + 30 * math.cos(ra), yc + 30 * math.sin(ra), SUN))
    # อิเล็กตรอนเคลื่อนที่สวนทิศกระแส (จาก − ไปทางล่างแล้ววน) — วางจุดเว้นระยะเท่ากันตามเส้นรอบวง
    per = 2 * ((R - L) + (B - T))
    def at(s):
        s %= per
        if s < R - L: return (L + s, B)
        s -= R - L
        if s < B - T: return (R, B - s)
        s -= B - T
        if s < R - L: return (R - s, T)
        s -= R - L; return (L, T + s)
    for i in range(26):
        x, y = at(i * per / 26 + 9)
        if (L - 20 < x < L + 20 and yc - 22 < y < yc + 22) or (abs(x - R) < 2 and abs(y - yc) < 20): continue
        b.append('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s"/>' % (x, y, FOAM))
    # ลูกศรทิศกระแส I (ตามเข็มนาฬิกาด้านบน: จาก + ไปทางขวา)
    b.append('<path d="M190 34 h40" stroke="%s" stroke-width="2.4"/><path d="M236 34 l-9 -5 v10 z" fill="%s"/>' % (SUN, SUN))
    b.append('<text x="182" y="39" fill="%s" font-family="Prompt, sans-serif" font-weight="700" font-size="15" text-anchor="end">I</text>' % SUN)
    return wrap(''.join(b), g)

ARTS = {'sound': art_sound(), 'electrostatics': art_electrostatics(), 'current': art_current()}
if __name__ == '__main__':
    p = os.path.join(ROOT, 'index.html')
    html = open(p, encoding='utf8').read()
    for k, svg in ARTS.items():
        html, n = re.subn(r'<!--ART:%s-->[\s\S]*?<!--/ART-->' % k, '<!--ART:%s-->%s<!--/ART-->' % (k, svg), html)
        if n != 1: raise SystemExit('ไม่พบตำแหน่ง ART:' + k)
    open(p, 'w', encoding='utf8').write(html)
    print('แทรกภาพ', len(ARTS), 'ภาพ')
