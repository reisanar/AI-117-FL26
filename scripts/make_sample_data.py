import argparse,random,pandas as pd
from common import DATA,log
backgrounds=['Computer Science','Statistics','Biology','Economics','Psychology','Information Science','Mathematics','Business','Public Policy','English']
homes=['Chapel Hill, NC','Durham, NC','Raleigh, NC','Charlotte, NC','Bogota, Colombia','Mumbai, India','Austin, TX','New York, NY']
songs=[("Texas Hold 'Em","Beyonce"),("Not Like Us","Kendrick Lamar"),("Good Luck, Babe!","Chappell Roan"),("Blinding Lights","The Weeknd"),("Clair de Lune","Debussy"),("Tití Me Preguntó","Bad Bunny"),("Fast Car","Tracy Chapman"),("Lovely Day","Bill Withers")]
defs=['AI is a computer system that learns patterns from data to make predictions or support decisions.','AI is software that imitates parts of human reasoning by recognizing patterns and generating responses.','AI is technology that turns data into actions, recommendations, or new content.','AI is a set of methods that helps machines perceive, learn, and adapt from examples.','AI is a tool for augmenting human judgment, creativity, and problem solving.']
feel=['It feels energetic and optimistic, like starting a project with momentum.','It reminds me of home and makes me think about memory and identity.','It is calm and focused, the kind of song I play when I need to think.','It feels joyful and social, like being in a room with friends.']
ap=argparse.ArgumentParser(); ap.add_argument('--n',type=int,default=42); args=ap.parse_args(); rows=[]
for i in range(args.n):
    title,artist=random.choice(songs)
    rows.append({'Timestamp':f'2026-08-{1+i%28:02d} 10:{i%60:02d}:00','What is your undergraduate background?':random.choice(backgrounds),'Where did you grow up? (city, state/country)':random.choice(homes),'In one sentence, define AI':random.choice(defs),'What excites you most about AI right now?':random.choice(['responsible AI','creative coding','data privacy','AI in education']),'What is the title of one song that has been on your mind recently?':title,'Who performs it?':artist,'In a sentence, describe how this song makes you feel':random.choice(feel)})
out=DATA/'raw_responses.csv'; pd.DataFrame(rows).to_csv(out,index=False); log(f'wrote synthetic data to {out} ({args.n} rows)')
