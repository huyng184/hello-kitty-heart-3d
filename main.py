# Hello Kitty + Heart 3D (no images) — Pygame + Unicode font + tiny heart (no emoji)
import math, random, pygame, sys

# -------- Settings --------
WIN_W, WIN_H = 900, 640
BG_TOP = (255, 230, 242)     # pastel hồng nhạt
BG_BOTTOM = (255, 214, 235)  # pastel hồng đậm
STAR_COUNT = 60
FPS = 60

TEXT_MAIN = "Cố lên baby, anh yêu em rất nhiều"
TEXT_SUB  = "You are purr‑fect"   # bỏ emoji, thay bằng tim vẽ code

HEART_ROT_SPEED = 1.8
HEART_BASE_SCALE = 0.42
HEART_BOB_AMPL = 10
KITTY_SCALE = 0.90

# Màu Kitty & UI
KITTY_WHITE = (255,255,255)
NO_PINK = (255,102,163)
NO_KNOT = (255,45,85)
NO_LIGHT = (255,174,203)
NO_STROKE = (210, 85, 135)
EYE = (0,0,0)
NOSE = (255,205,70)

# Font ưu tiên (có hỗ trợ tiếng Việt)
FONT_CANDIDATES = [
    "Segoe UI", "Arial", "Tahoma", "Verdana",
    "Roboto", "Noto Sans", "DejaVu Sans", "Helvetica Neue"
]

# -------------------------- Helpers --------------------------

def load_font(size, bold=False):
    path = pygame.font.match_font(FONT_CANDIDATES, bold=bold)
    if path:
        return pygame.font.Font(path, size)
    return pygame.font.SysFont(None, size, bold=bold)

def draw_vertical_gradient(surface, top_color, bottom_color):
    h = surface.get_height()
    w = surface.get_width()
    for y in range(h):
        t = y / (h - 1)
        r = int(top_color[0]*(1-t) + bottom_color[0]*t)
        g = int(top_color[1]*(1-t) + bottom_color[1]*t)
        b = int(top_color[2]*(1-t) + bottom_color[2]*t)
        pygame.draw.line(surface, (r,g,b), (0,y), (w,y))

def make_stars(n):
    stars = []
    for _ in range(n):
        x = random.randint(18, WIN_W-18)
        y = random.randint(18, WIN_H-160)
        r = random.choice([1,1,1,2,2,3])
        phase = random.random() * math.tau
        stars.append([x,y,r,phase])
    return stars

def draw_stars(surface, stars, t):
    def clamp_color(val):
        return max(0, min(255, int(val)))
    for x, y, r, phase in stars:
        br = 0.55 + 0.45 * math.sin(t*1.2 + phase*3)
        r_c = clamp_color(255*(0.7+0.3*br))
        g_c = clamp_color(255*(0.7+0.2*br))
        b_c = clamp_color(255*(0.7+0.4*br))
        pygame.draw.circle(surface, (r_c, g_c, b_c), (x, y), r)

def draw_tiny_heart(surface, center, size, color, outline=None):
    """Vẽ 1 trái tim nhỏ bằng 2 hình tròn + tam giác (không dùng emoji)."""
    x, y = center
    r = max(1, size // 2)
    # hai “núm” tròn
    pygame.draw.circle(surface, color, (x - r, y - r), r)
    pygame.draw.circle(surface, color, (x + r, y - r), r)
    # tam giác đáy nhọn
    pts = [(x - size, y - r), (x, y + size), (x + size, y - r)]
    pygame.draw.polygon(surface, color, pts)
    if outline:
        pygame.draw.circle(surface, outline, (x - r, y - r), r, 1)
        pygame.draw.circle(surface, outline, (x + r, y - r), r, 1)
        pygame.draw.polygon(surface, outline, pts, 1)

# -------------------------- Kitty & Heart --------------------------

def kitty_shape(surface, center, scale=1.0):
    cx, cy = center
    def sc(v): return int(v*scale)

    body = pygame.Rect(0,0, sc(260), sc(220))
    body.center = (cx, cy+sc(130))
    pygame.draw.rect(surface, KITTY_WHITE, body, border_radius=sc(40))

    left_arm = pygame.Rect(0,0, sc(120), sc(160)); left_arm.center = (cx-sc(180), cy+sc(150))
    right_arm= pygame.Rect(0,0, sc(120), sc(160)); right_arm.center= (cx+sc(180), cy+sc(150))
    pygame.draw.ellipse(surface, KITTY_WHITE, left_arm)
    pygame.draw.ellipse(surface, KITTY_WHITE, right_arm)

    head = pygame.Rect(0,0, sc(540), sc(460)); head.center = (cx, cy)
    pygame.draw.ellipse(surface, KITTY_WHITE, head)

    pygame.draw.polygon(surface, KITTY_WHITE, [(cx-sc(240), cy-sc(140)), (cx-sc(140), cy-sc(260)), (cx-sc(100), cy-sc(100))])
    pygame.draw.polygon(surface, KITTY_WHITE, [(cx+sc(240), cy-sc(140)), (cx+sc(140), cy-sc(260)), (cx+sc(100), cy-sc(100))])

    pygame.draw.ellipse(surface, (0,0,0), (cx-sc(90), cy-sc(40), sc(40), sc(60)))
    pygame.draw.ellipse(surface, (0,0,0), (cx+sc(50), cy-sc(40), sc(40), sc(60)))

    pygame.draw.ellipse(surface, NOSE, (cx-sc(17), cy+sc(20), sc(34), sc(26)))

    for dy in (-sc(40),0,sc(40)):
        pygame.draw.line(surface, (0,0,0), (cx-sc(130), cy+dy), (cx-sc(200), cy+dy-sc(10)), sc(5))
        pygame.draw.line(surface, (0,0,0), (cx-sc(130), cy+dy), (cx-sc(200), cy+dy+sc(10)), sc(5))
    for dy in (-sc(40),0,sc(40)):
        pygame.draw.line(surface, (0,0,0), (cx+sc(130), cy+dy), (cx+sc(200), cy+dy-sc(10)), sc(5))
        pygame.draw.line(surface, (0,0,0), (cx+sc(130), cy+dy), (cx+sc(200), cy+dy+sc(10)), sc(5))

    bow_c = (cx+sc(200), cy-sc(120))
    left = pygame.Rect(0,0, sc(120), sc(80)); left.center = (bow_c[0]-sc(60), bow_c[1])
    right= pygame.Rect(0,0, sc(120), sc(80)); right.center= (bow_c[0]+sc(60), bow_c[1])
    pygame.draw.ellipse(surface, NO_PINK, left)
    pygame.draw.ellipse(surface, NO_PINK, right)
    pygame.draw.circle(surface, NO_KNOT, bow_c, sc(22))
    pygame.draw.circle(surface, NO_LIGHT, (bow_c[0]+sc(12), bow_c[1]-sc(10)), sc(6))
    pygame.draw.ellipse(surface, NO_STROKE, left, sc(2))
    pygame.draw.ellipse(surface, NO_STROKE, right, sc(2))

def heart_points(n=420):
    pts = []
    for i in range(n):
        t = 2*math.pi*i/n
        x = 16*math.sin(t)**3
        y = 13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)
        pts.append((x, -y))
    return pts

def transform_points(pts, cx, cy, scale_x, scale_y):
    return [(cx + x*scale_x, cy + y*scale_y) for x, y in pts]

def draw_heart(surface, center, angle_deg, base_scale=1.0):
    cx, cy = center
    c = math.cos(math.radians(angle_deg))
    sx = max(abs(c), 0.12) * base_scale * 12
    sy = (0.96 + 0.04*math.cos(math.radians(angle_deg))) * base_scale * 12
    pts = transform_points(HEART_CACHE, cx, cy, sx, sy)

    # Glow viền
    for w, col in [(10, (255,143,179)), (6, (255,143,179)), (3, (255,143,179))]:
        pygame.draw.aalines(surface, col, True, pts)

    # Fill
    pygame.draw.polygon(surface, (255,77,136), pts)

    # Nửa sau — gợi cảm giác mặt sau
    if c < 0:
        pygame.draw.aalines(surface, (255,170,190), False,
                            [(cx, cy - 60*base_scale), (cx, cy + 60*base_scale)])

    # Highlight
    hx = cx + int(36 * c * 0.7 * base_scale)
    hy = cy - int(40 * base_scale)
    pygame.draw.circle(surface, (255, 234, 245), (hx, hy), int(6*base_scale))

HEART_CACHE = heart_points()

# -------------------------- Main --------------------------

def main():
    pygame.init()
    pygame.display.set_caption("Hello Kitty Heart 3D 💗 (no images)")
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    clock = pygame.time.Clock()

    # Nền gradient + khung viền
    bg = pygame.Surface((WIN_W, WIN_H)).convert()
    draw_vertical_gradient(bg, BG_TOP, BG_BOTTOM)
    pygame.draw.rect(bg, (255,255,255), (10,10, WIN_W-20, WIN_H-20), width=4, border_radius=18)

    stars = make_stars(STAR_COUNT)

    font_main = load_font(36, bold=True)
    font_sub  = load_font(22, bold=False)

    t = 0.0
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        t += dt
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_q)):
                running = False

        screen.blit(bg, (0,0))
        draw_stars(screen, stars, t)

        # Kitty
        kitty_cx, kitty_cy = WIN_W//2, int(WIN_H*0.42)
        kitty_shape(screen, (kitty_cx, kitty_cy), scale=KITTY_SCALE)

        # Trái tim xoay + nhún
        angle = (t * 60 * HEART_ROT_SPEED) % 360
        c = math.cos(math.radians(angle))
        bob_y = int(math.sin(t*2.0) * HEART_BOB_AMPL)

        # Bóng dưới tim
        shadow_w = int(180 * (0.45 + 0.55*abs(c)))
        shadow_surf = pygame.Surface((shadow_w, 18), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (232,166,192,120), shadow_surf.get_rect())
        screen.blit(shadow_surf, (WIN_W//2 - shadow_w//2, int(WIN_H*0.72)))

        # Vẽ tim ở “tay ôm”
        heart_center = (WIN_W//2 + int(6*c), int(WIN_H*0.60) + bob_y)
        draw_heart(screen, heart_center, angle, base_scale=HEART_BASE_SCALE*KITTY_SCALE)

        # Nơ treo phía trên
        bow_cx, bow_cy = WIN_W//2, int(WIN_H*0.14)
        pygame.draw.ellipse(screen, NO_PINK, (bow_cx-90, bow_cy-35, 120, 70))
        pygame.draw.ellipse(screen, NO_PINK, (bow_cx-30, bow_cy-35, 120, 70))
        pygame.draw.circle(screen, NO_KNOT, (bow_cx, bow_cy), 20)
        pygame.draw.circle(screen, NO_LIGHT, (bow_cx+12, bow_cy-8), 6)

        # Text + tim nhỏ (thay emoji)
        main_surf = font_main.render(TEXT_MAIN, True, (255, 45, 85))
        sub_surf  = font_sub.render(TEXT_SUB,  True, (255, 92, 138))
        main_rect = main_surf.get_rect(center=(WIN_W//2, WIN_H-58))
        sub_rect  = sub_surf.get_rect(center=(WIN_W//2, WIN_H-28))

        pill_w = int(main_rect.width*1.12)
        pill = pygame.Surface((pill_w, 72), pygame.SRCALPHA)
        pygame.draw.rect(pill, (255,255,255,130), pill.get_rect(), border_radius=18)
        screen.blit(pill, (WIN_W//2 - pill_w//2, WIN_H-82))
        screen.blit(main_surf, main_rect)
        screen.blit(sub_surf, sub_rect)

        # Trái tim hồng nhỏ cạnh dòng phụ (không emoji)
        pad = 10
        tiny_center = (sub_rect.right + pad + 8, sub_rect.centery - 1)
        draw_tiny_heart(screen, tiny_center, size=14, color=(255, 92, 138), outline=(255,143,179))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
