import re
from unidecode import unidecode


REPEAT_REGEX = re.compile(r"((.)\2*)")


def remove_repeated_characters(expr):
    # limit number of repeated letters to 3. For example loooool --> loool
    string_not_repeated = ""
    for item in REPEAT_REGEX.findall(expr):
        if len(item[0]) <= 3:
            string_not_repeated += item[0]
        else:
            string_not_repeated += item[0][:3]
    return string_not_repeated


CAMEL_CASE_REGEX = re.compile(
    r".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)"
)


def camel_case_split(expr):
    # HelloWorld -> Hello World
    matches = CAMEL_CASE_REGEX.finditer(expr)
    return " ".join([m.group(0) for m in matches])


NOT_LETTERS = re.compile(r"[^a-zA-Z]")
MANY_SPACES = re.compile(r" +")
URL = re.compile(r"http\S+", flags=re.MULTILINE)
TWITTER_HANDLE = re.compile(r"@\S+", flags=re.MULTILINE)
POSTS_SEPARATOR = re.compile(r"\|\|\|", flags=re.MULTILINE)

HASHTAG = re.compile(r"#(\S+)")


def repl_hashtag(m):
    content = m.group(1)
    return camel_case_split(content)


def format_text(text):
    try:
        # Unfold posts.
        text = unidecode(POSTS_SEPARATOR.sub(" ", text))
        # Remove URLs.
        text = unidecode(URL.sub("", text))
        # Remove Twitter handles (usernames).
        text = unidecode(TWITTER_HANDLE.sub("", text))
    except Exception:
        print(text)
        raise

    text = HASHTAG.sub(repl_hashtag, text)
    text = NOT_LETTERS.sub(" ", text)  # only keep words
    text = MANY_SPACES.sub(" ", text).lower()  # remove big spaces
    text = remove_repeated_characters(text)
    return text


if __name__ == "__main__":
    # posts = "http://www.youtube.com/watch?v=qsXHcwe3krw|||http://41.media.tumblr.com/tumblr_lfouy03PMA1qa1rooo1_500.jpg|||enfp and intj moments  https://www.youtube.com/watch?v=iz7lE1g4XM4  sportscenter not top ten plays  https://www.youtube.com/watch?v=uCdfze1etec  pranks|||What has been the most life-changing experience in your life?|||http://www.youtube.com/watch?v=vXZeYwwRDw8   http://www.youtube.com/watch?v=u8ejam5DP3E  On repeat for most of today.|||May the PerC Experience immerse you.|||The last thing my INFJ friend posted on his facebook before committing suicide the next day. Rest in peace~   http://vimeo.com/22842206|||Hello ENFJ7. Sorry to hear of your distress. It's only natural for a relationship to not be perfection all the time in every moment of existence. Try to figure the hard times as times of growth, as...|||84389  84390  http://wallpaperpassion.com/upload/23700/friendship-boy-and-girl-wallpaper.jpg  http://assets.dornob.com/wp-content/uploads/2010/04/round-home-design.jpg ...|||Welcome and stuff.|||http://playeressence.com/wp-content/uploads/2013/08/RED-red-the-pokemon-master-32560474-450-338.jpg  Game. Set. Match.|||Prozac, wellbrutin, at least thirty minutes of moving your legs (and I don't mean moving them while sitting in your same desk chair), weed in moderation (maybe try edibles as a healthier alternative...|||Basically come up with three items you've determined that each type (or whichever types you want to do) would more than likely use, given each types' cognitive functions and whatnot, when left by...|||All things in moderation.  Sims is indeed a video game, and a good one at that. Note: a good one at that is somewhat subjective in that I am not completely promoting the death of any given Sim...|||Dear ENFP:  What were your favorite video games growing up and what are your now, current favorite video games? :cool:|||https://www.youtube.com/watch?v=QyPqT8umzmY|||It appears to be too late. :sad:|||There's someone out there for everyone.|||Wait... I thought confidence was a good thing.|||I just cherish the time of solitude b/c i revel within my inner world more whereas most other time i'd be workin... just enjoy the me time while you can. Don't worry, people will always be around to...|||Yo entp ladies... if you're into a complimentary personality,well, hey.|||... when your main social outlet is xbox live conversations and even then you verbally fatigue quickly.|||http://www.youtube.com/watch?v=gDhy7rdfm14  I really dig the part from 1:46 to 2:50|||http://www.youtube.com/watch?v=msqXffgh7b8|||Banned because this thread requires it of me.|||Get high in backyard, roast and eat marshmellows in backyard while conversing over something intellectual, followed by massages and kisses.|||http://www.youtube.com/watch?v=Mw7eoU3BMbE|||http://www.youtube.com/watch?v=4V2uYORhQOk|||http://www.youtube.com/watch?v=SlVmgFQQ0TI|||Banned for too many b's in that sentence. How could you! Think of the B!|||Banned for watching movies in the corner with the dunces.|||Banned because Health class clearly taught you nothing about peer pressure.|||Banned for a whole host of reasons!|||http://www.youtube.com/watch?v=IRcrv41hgz4|||1) Two baby deer on left and right munching on a beetle in the middle.  2) Using their own blood, two cavemen diary today's latest happenings on their designated cave diary wall.  3) I see it as...|||a pokemon world  an infj society  everyone becomes an optimist|||49142|||http://www.youtube.com/watch?v=ZRCEq_JFeFM|||http://discovermagazine.com/2012/jul-aug/20-things-you-didnt-know-about-deserts/desert.jpg|||http://oyster.ignimgs.com/mediawiki/apis.ign.com/pokemon-silver-version/d/dd/Ditto.gif|||http://www.serebii.net/potw-dp/Scizor.jpg|||Not all artists are artists because they draw. It's the idea that counts in forming something of your own... like a signature.|||Welcome to the robot ranks, person who downed my self-esteem cuz I'm not an avid signature artist like herself. :proud:|||Banned for taking all the room under my bed. Ya gotta learn to share with the roaches.|||http://www.youtube.com/watch?v=w8IgImn57aQ|||Banned for being too much of a thundering, grumbling kind of storm... yep.|||Ahh... old high school music I haven't heard in ages.   http://www.youtube.com/watch?v=dcCRUPCdB1w|||I failed a public speaking class a few years ago and I've sort of learned what I could do better were I to be in that position again. A big part of my failure was just overloading myself with too...|||I like this person's mentality. He's a confirmed INTJ by the way. http://www.youtube.com/watch?v=hGKLI-GEc6M|||Move to the Denver area and start a new life for myself."
    posts = "I admire you humor, INTP. So, it would be great if you got out of your bed, took a shower, and shared it with someone once in a while. How about a friend?  No, not a friend on WoW. A real friend....|||... Oh, INTP.  http://replygif.net/i/661.gif|||Ew, what are 'feels'? Are they a disease? Keep your hands to yourself, ENFP. Don't come any closer!|||DISNEY...  ESFJ http://media.giphy.com/media/Pgb4zlVQqnUB2/200.gif  ENFP http://media1.giphy.com/media/4Sup4tYbf3Spy/200.gif  ESTP http://media3.giphy.com/media/11dKPOwwpBToli/200.gif|||ESTx http://fuza.ru/uploads/posts/2012-11/1351870798_gifaki-gifki-smeshnye-gifki-gifki-kote_62214790.gif  INTP http://dsjvpv76ko1eo.cloudfront.net/uimg/4b570b191ca6046025f6e0ee57688d74.600x|||INTP. http://cdn.lolbrary.com/2013/12/6/lolbrary.com_54945_1386368749.gif  ENTJ. http://www.focusst.org/forum/attachments/off-topic/20999d1380281556-share-your-favorite-gif-beiber.gif  ESTP....|||ISxJ http://media0.giphy.com/media/TT8rdXzeXiNri/200.gif  ESFJ http://media3.giphy.com/media/IvjjgsEhnLCzm/200.gif  ExTP http://media1.giphy.com/media/125dLiH6FOeBAA/200.gif  ISTP|||ISTP?  Guess has nothing to do with the song. But he's on a motorcycle, alone, with a gun... http://24.media.tumblr.com/tumblr_lkysjs7J2t1qixleeo1_500.gif|||EDIT-Beat me to it, ENTP.  Shh. I'm not here. Ignore this.|||INFJ, insult that ENTP http://annakie.com/cpg/albums/userpics/10002/Be-a-Man.gif. I'm sure it won't kill his ego. An ENTP's ego is too big to burst.|||Childhood.  INTP http://media2.giphy.com/media/R2WnCkxBf5u0w/200.gif http://media1.giphy.com/media/5hEYTJT7p2tMc/200.gif  ENTP http://media3.giphy.com/media/IWdguYygkigaA/200.gif...|||Well, polar opposites of each of these may be something like burnt bread or an empty fridge. Do you find joy with either of those things? I know I do....|||http://static.fjcdn.com/gifs/trippy+gif+3.+different+gif+yet+still+mind+blowing_ba8bb2_3699999.gif You INFJs. Such amazing philosophers :frustrating:.|||MBTI Types DEALING WITH FLIRTING/LOVE INTERESTS...  ESTP http://25.media.tumblr.com/6a20b021f971a58aa444049d922dda51/tumblr_my4mbg9i3T1r1sl7xo1_500.gif  INTP...|||Ever wanted to see what an INTJ is on the inside? http://25.media.tumblr.com/tumblr_m6tv8blIXF1r7psebo1_500.gif|||Leave an ISFP alone and... http://i.imgur.com/i6lzJ.gif  ENTPs know what they're doing... http://i.imgur.com/y0Rmf.gif  ESFPs......|||Test Survey 2.0  1. talkative or contemplative 2. sociable or solitary 3. outgoing or reserved  4. pragmatic, intellectual, idealistic, sensitive. 5. curious, realistic, imaginative,...|||Sure. 1. outgoing, reserved 2. talkative, contemplative 3. sociable, solitary ((Nehh...depending on who I'm with.)) 4. realistic, philanthropic, idealistic, theoretical. 5. pragmatic,...|||Find your gif, and copy the URL. http://s13.postimg.org/gvtt1b387/SCREEN.png  Click on the Insert Image icon third from the right of the message options......|||MOSTLY INSULTING GIFs  ISTJ, INTJ... http://25.media.tumblr.com/tumblr_mantz0wf341rr3l61o1_500.gif  ESFP, ESTP... http://media.giphy.com/media/WhAyEpYKSH1lu/giphy.gif  INFP, INTP......|||I said I don't know because I wanted some feedback. You seem to know.|||I'm an ISTP. The T over F preference is low ((or I have developed Fe?)).  1.) Going to bed knowing you can sleep for as long as you want OR a compliment from a stranger.   2.) The smell of...|||I agree, and I really doubt humans will ever have real proof. But they probably won't ever be able to disprove the theory, either. There's always the what if's. I sort of feel better with it...|||So you're saying people are similar to robots, they cannot choose what they do or do not do, we're all just programmed to do these functions?|||1: What's your MBTI Type? ISTP 2: What's your Gender? Female 3: Are you the eldest child, middle child, or youngest child? Youngest. 4: How do you learn: Hands-on, seeing, or auditory?...|||Shhhh.|||Drake- ESxP ((ISTP sounds pretty off.)) Josh- ENFPish ((Wild guess. Pretty sure he's an F.)) Megan- ENTJ Mindy- ENTJ Helen- xxTJish?|||Club Penguin... We should make a Webkinz one, too, then :ninja:.  Fine. I'll do it. 1- ISTPish 2- ESFP 3- ESTP 4- ENFP 3- ISFJ|||INTJness.|||You can't ever truly be sure. People are more complicated than their types. You may see yourself one way, but can you ever truly be sure that's who you are? Nah. We can't even be sure that MBTI...|||The best mates/friends for her type, you're saying?|||A bit INFJ.|||INFJ sounds right for that one. Poetic. Mysterioussss...|||ENFPness.|||INFPish.|||LOOOOVE GIFs for MBTI  INTJs, INTPs... http://data.whicdn.com/images/60916177/large.gif   INTJs... http://31.media.tumblr.com/tumblr_m4gh5n5iTr1rn95k2o1_500.gif  ESTP, ESFP...|||Yeah, that five paragraph opinion sounds appropriate for a GIF thread... :ninja: ((To post a GIF, upload it to a site that gives you the direct link, then put that link inbetween the code . I use...|||You know you're a Sensor when you've given numbers their own personalities, and like/dislike them because of that.  Am I the only one who thinks 9 is arrogant? It thinks it's basically the great...|||ISFP. On tests, my percentage for Thinking/Feeling preference is low, about 10%, 5%, sometimes 2%.  I easily feel empathy for others, no matter who they are, which most claim an ISTP is incapable...|||I can see the ENTJ. Something about the sassy humor. Not sure I know enough about ENTXs to give you something better.   Oh. That's a pretty decent reason. :ninja:|||ISTP. They're known to have that sort of cold intense look as their default face. Unless you were trying to look badass. Maybe ISFP.|||INFJ. It seems mysterious yet with meaning. Curious.  It could be interpreted as many different things. Why'd you pick it?   You're supposed to rate the avatar above you. Selfish. You deserve...|||Alright guys...I didn't think it would come to this. But you've forced me to...   Classic ESTP/ESFP Hangout http://s21.postimg.org/5quosbriv/stud2.gif http://s11.postimg.org/x1ydjfdo3/stud5.gif...|||An INTJ.|||Only had a few on my computer. Us Quiet Types... http://s14.postimg.org/aaia1y3s1/friends.jpg  ENFP, ENFJ, In the ISFPs mind, and any other innocent Romantics......|||I like wearing black, too. Hard to see dirt in and I just like the look of it in general. Not all black, although I don't mind being in all black ((I look so ninja...)), people in school tend to...|||HAHAHAHAHAHAH. So original :ninja:. Couldn't help yourself, huh?|||ISFP OOOOOOOOOOOOOOOOOOOOOOH. Because of the mysterious yet kind nature of the name? I suck at this.|||Spy: ISTP Villain: INTJ Rock Star: ESFP/ESTP Knight: ISTJ/ESTJ Princess: ISFP Bodyguard: ISTP Heir to a Large Company: ENTJ Martyr: ENFJ/INFJ Soldier: ISTJ Overprotective Parent: ISFJ/INFJ|||I'd make them a hamburger."
    print(format_text(posts))
