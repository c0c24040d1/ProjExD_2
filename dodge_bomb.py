import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct:pg.Rect) -> tuple[bool,bool]:
        yoko, tate = True, True
        if rct.left < 0 or WIDTH  < rct.right:
            yoko = False
        if rct.top < 0 or HEIGHT < rct.bottom:
            tate = False
        return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    tmr = 0

    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct=bb_img.get_rect()
    bb_rct.centerx=random.randint(0,WIDTH)
    bb_rct.centery=random.randint(0,HEIGHT)

    vx, vy = +5,+5

    clock = pg.time.Clock()
    acl=0

    fonto = pg.font.Font(None,100)
    txt = fonto.render("Game Over",True ,(255, 0 ,0))
    # def calc_orientation(org: pg.Rect, dst: pg.Rect,current_xy: tuple[float, float])->tuple[float,float]:
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            screen.blit(txt , [300,200])
            print("Game Over")
            pg.display.update()
            return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        if tmr <=10000:
            acl=1+tmr//500
            avx=vx*acl
            avy=vy*acl
            bb_img = pg.Surface((20*acl,20*acl))
            pg.draw.circle(bb_img,(255,0,0),(10*acl,10*acl),10*acl)
            bb_img.set_colorkey((0,0,0))

        bb_rct.move_ip(avx,avy)
        # vx, vy = calc_orientation(bb_rct2,kk_rct,(vx,vy))
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx*=-1
        if not tate:
            vy*=-1
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
