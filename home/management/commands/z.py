from collections import UserList
from pprint import pprint
from urllib.request import DataHandler
from django.core.management.base import BaseCommand
from home.models import user_details
from .functions_file.function_msg import *
import pandas as pd 
# from telethon.errors.rpc_error_lis import PhoneNumberBannedError # exception during client.send_code_request()
COMMENTS_ = ["XANA Metaverse is here to stay 🚀🚀🚀🚀","Cant wait for the first duel in the Metaverse!","Niicceeee fun time!","That’s wonder why XANA is the best on web3.0✌🏼","XANA Metaverse will be the next level of the internet","Yeahhh 🙌 Sooo cool!!","It will be a platform for innovation, creativity, and expression. 🙌","How amazingly this platform is making the way into entertainment industry!!","I can't wait for attending a concert with unlimited capacity here!","Ooo! It's really an amazing decision to be a part of XANA🙌","XANA is a medium that has the potential to change the world.","Love this project ❤ one of the best communities of the crypto gaming 🔥","I'm super excited to visit different places, and interact with other people in the metaverse.","The Metaverse with everything for everyone","Immersive experiences that feel like the future","Amazing! Love it how I can interact with everyone inside, just like the real world.","Feel like I'm living inside a game or movie!","The best VR experience on the planet","I was blown away by how real it felt","you really have to experience it to understand","It feels so reaaalll that it scares you but at the same time excites you","This place is INCREDIBLE!!!!!! Like holy crap","truly social VR - it's awesome...it's wild.","Incredible team building experience","The best VR experience period","Superb!! Expanding the possibilities of human experience through immersive technology.","Is the XANA open to everybody now?","Perfect place to use your NFTs🔥","Buzzing with excitement over this one! Amazing Features!✌🏼","Let's go🔥🔥","XANA Metaverse is the future!","When there is more than to do just walk in the lobby!","Bringing security to XANA is an exciting step. Thanks XANA Metaverse!!","Yeah!! Love it!! EPIC!!","This is so dope Metaverse!🙌","Let's go to experience a magnificent Metaverse!","This shows the good that can emerge from fun Metaverse projects like XANA","Perfect world🔥🔥","Hi, How can I join? should I join it via Desktop or Mobile?","Thanks XANA I need an avatar for Metaverse and you made it happen for me!","How much is alphha pass?","My dream is to own land in the Sandbox and build my Skyland there, Yeah, hope i can make it possible here!","Loving the alpha!","Great job, entire team!","Amazing, I'm coming too are you ready?","The NFT space is going to be very big","This is really an amzing project, love to be a part of this platform!","So good and intresting. I wonder how they created this Metaverse.","Anyone here knows how to host my concert in the Metaverse?","Love this concept to meet and interact virtually.","XANA the bestHey, when does the mobile version come out?","Does XANA work on Oculus?","We want a detailed video on how to use XANA world?","That's awesome🔥","That's a cool feature, thank you for that.","Stay one step ahead, that's the key.","XANA going to blow up","There are many great opportunities. Like creating NFTs or as a bigger investment, purchasing a land in Metaverse like XANA","This is amazing, I can't believe I can use it now","Bigger moves🔥","XANA Metaverse is the truth","Really enjoying all the features, especially the dancing part by avatars.","Let's go for the long run in XANA🔥","Yes this is so cool, amazing team.","Wooow🔥","Cheers for the decentralized world","Excited to experience","Get ready to rock the techno music stage at XANA Metaverse!","Awaiting for the event!","This looks great, cant wait to buy it!","Ah what an amazing NFT by such famous artist.","Dude you are creating a whole new world for us!","I am so excited about this AMA","I have enjoyed the interactive session with such amazing CEO🌹.","This NFT series is really alluring & I am absolutely going to whitelist myself.","Loving this futuristic update in the platform!🙌","XANA is climbing the success stair steadily and it is going ti be really huge.","Metaverse is the future of the Internet and XANA is proving that with each amazing update👌.","wow! this giveway is actually really fun, let's enjoy this!","XANA experience is so much fun with avatar customization!","Many big business are coming to XANA to leverage its potential.","I never thought it would be so much fun to enter the Metaverse but XANA made it possible.","Linking #NFTs with the metaverse space allows users to enter a new world. It will emerge as a virtual copy of the physical world but with more possibilities.","The ability to earn by playing a game has transformed the lives of many players.","The world is going to witness the #Metaverse as the souped-up version of #VR.","NFTs are revolutionizing Metaverse gaming with the earning opportunity for players.","Creating personlized 3D avatars in the Metaverse would be so much fun, I love this update by XANA team.","Haven't seen such amazing NFT ever. This anime character is my favourite hero.","I love this update, this will make the Metaverse an entertaining space.✌","This is really great for businesses to virtually interact with the audience.","This NFT series is going to get huge attention, I can bet on that.","What? Really this just sold out in few seconds. I missed it this time.","Enjoying my time in the Metaverse with the 3D avatar and activities.","XANA is hitting the success road with this recent update.","I am amazed to see this attractive world at XANA Metaverse.","Amazing! I’m waiting for the alpha release! A question, when will you create giveaways for the same?","You guys are killing it! Keep it up and you'll be masters of the Metaverse! 🙌","This is really insane. I am a VR freak and I love this update.","Keep it up guys🔥🚀","I am excited to relish the best #VR experiences with #XANA Metaverse.","Metaverse is unlocking doors of a new digital world for people. Businesses can leverage this as an advanced opportunity to overgrow their engagement, sales & brand value.","The era of Metaverse is Here with XANA!","you are creating a next level platform, all my support to you guys!🎉","Just check-out this amazing NFTs, its really fun.🐱‍🚀","XANA metaverse game is creating new milestone for everyone","I played in the XANA with my friends, we all loved it!","AstroBoy is the real hero, Can't thank you enough for launching its NFT!","I am whitelisting rightaway for this NFT launch, this is what I have been waiting for all these years.","I can not miss this NFT launcc, alredy signed up for the whitelist and set an alarm for the launch time.","Can I display my NFTs at XANA?","Metaverse holds limitless opportunities for us!","I have registered for this giveaway, Hoping to win this time!","So excited for this NFTs, they have amazing design.","Genesis NFTs are more advanced than ever, I have never seen such unique concept!😃","This conceptualized genesis NFTs are super fun!✨","This is a great project!😍","Can't wait for more updates!!","Thank you so much for giving us this great opportunity. We are all so excited about this great event!","Great Project! Hope this project is a success I'm so excited!","Wow, cool! Keep working guys! All support for your team!💃🏻","Your investment should be rewarding in the Metaverse #xana","Make sure you know and understand enough about NFTs before buying your first NFT to use in metaverse. #xana","The ways suited to confidence are familiar to me for metaverse XANA, but not those that are suited to familiarity.","The metaverse evolves, fractally and forever.","What is inevitable not death but change with the metaverse like #XANA.","In the Metaverse, you can be a warrior prince. #XANA","I just found virtual amusement park with no size limit only in Metaverse #XANA.","Unlimited creativity in the digital world can be realized with Metaverse #XANA","No doubt #XANA Metaverse provide new experiences and opportunities for creators, gamers and artists.","#XANA Metaverse is the gateway to most digital experiences.","#XANA metaverse can be a key component of all physical experiences.","#XANA is the next great workforce platform. Great work.","#XANA provide great multitasking opportunities for its users. Keep it up.","Yeyy I can work, play, do business, and socialize with other people friend and family.","I am able to transcend all that is seen and known to exist through #XANA","A lovely ecosystem that can find elements, creations, experiences, and interactions. #XANA","In #XANA Metaverse I can use persistent space.","With #XANA I can create a great new world digitally.","Have fun.","Great work, keep it up <3","#XANA Metaverse is not only a place to game but entertainment. Love you guys :-*","Everyone including me is getting into the virtual world craze whether you know it or not. ","The more I use #XANA metaverse the less I feel like I am alone.","Yes, #XANA metaverse is here, it’s time to create.","Today’s runway show was very meta. #XANA","What a beautiful virtual world #XANA","Welcome to the world of tomorrow #XANA","Put your feet up and enjoy a break in this virtual world #XANA","We are a force to be reckoned with in the #XANA","Great effort","Love your concept and creativity","Let the future happen with #XANA. It’s interesting. ""I made the money with #XANA","Let's impliment the art of thinking independently together.","Live your best life in a virtual world where anything is possible. #XANA","Hello friends! Come fly with me in Virtual Reality via #XANA","Your vision is so inspiring man, I am gonna follow your tips for success!","Relax your mind with entertaining virtual world #XANA","I really believe that the virtual world #XANA mirrors the physical world.","One day the virtual world #XANA might win over the metaverses.","Photography is a kind of virtual reality, and it helps if you can create the illusion of being in an interesting virtual world. #XANA","I think that in an increasingly virtual world #XANA, lovingly produced artefacts are at a premium.","The #XANA virtual world is not the enemy.","I would like to live in the Virtual world #XANA.","You are the future guys","Amazing features <3","Lovely 3D Envirenment <3","Get amused with XANA.","Can I Earn money through XANA?","All my support is for you. Lovely work.","Wow everything is virtual. Love this virtual world #XANA 😍","Keep on growing 💗","Welldone guys 👍","Metaverse #XANA is a boon for businessmen and entertainer. 🤲","My friends on #XANA not only share fun but also share feelings. 😍","The best things in life can be experienced virtually. #XANA 😀","I know the virtual world #XANA reflect the physical world. 🔥","I never thought owning digital assets within the Metaverse would be a fun","Market giants are moving to the Metaverse ecosystem, I believe this is the future of the Internet.","Can't wait to see what you guys have in store!💃🏻","I can't wait to own land and digital assets in the form of NFTs in this XANA metaverse.","A metaverse to unite, but not fight! You in?🤩","I love this one so much! Keep going it‘s really beautiful 💖🔥😍🙌🥰","Its a loving project, really appreciating your work. 👌","I appreciate you more because of the roadmap you guys followed. Thanks to XANA. ❤️","Can't wait to see what you guys have featured it 😀","This is such a great idea for a site! I'm going to sign up right now!😍","I've been following your company for a while, and it seems like you are on the forefront of bringing NFTs to the masses.","Happines in XANA measured by our desires😇","I am really exited to be the part of XANA metaverse 🤩","Great project wow 😍","I like to connect to people in the virtual world #XANA, exchanging thoughts and ideas, when in the physical world we might never have the opportunity to cross paths.","Unfortunately, no one can be told what the Matrix is. You have to see its example #XANA.","Virtual reality is the first step in a grand adventure into the landscape of the imagination. #XANA world","Get amused with #XANA.🤩","Come fly with me in Virtual Reality in XANA. ✈️","Relaxing, & putting my feet up and enjoying a break in the XANA.😄","Virtual world #XANA is fascinating ❤️‍🔥","Virtual reality is like dreaming with your eyes open. 😴","#XANA is a medium, a means by which humans can share ideas and experiences.","There's nobody who works in VR saying, ","Oh, I'm bored with this." "Everybody comes back. 😁","I appreciate your determination in showing us a great NFTs. Great work. 💖🔥😍","More and more people are reaching you, Great work ❤️‍🔥","Words cannot express my feelings, nor my thanks for all your efforts XANA team. 💖🔥😍","XANA's teams thoughtfulness & hardwork will always be remembered.🙌🙌","VR will never look real until they learn how to put some entertainment in it. 😄","Most people are awaiting Virtual Reality; I'm awaiting virtuous reality. 😇#XANA","When virtual reality gets cheaper than society become reward. 😄","We are yet to see a person who has experienced #XANA and emerged unconvinced. 👍","One day the virtual world #XANA might win over the real world. 🙏","Poor VR takes you straight to puke town, and nobody experienced that in #XANA 😇","When you think about creating content for virtual reality then must try #XANA.","Let's be the part of Entertaining XANA metaverse 🤩","This looks great, cant wait to buy it!","Great metaverse #XANA 😍","Let's celebrate my birthday in virtual world #XANA 🎂","The good news is that virtual world is here. #XANA 😍","I like to connect to people in the virtual world, exchanging thoughts and ideas.😍 #XANA","Virtual world #XANA is going to be the foundation of future communication.❤️‍🔥","I loved your futuristic approach. 💖🔥😍🙌"]

class Command(BaseCommand):
    help = 'send message as per csv'

    def handle(self,*args, **kwargs):
        user_li = user_details.objects.all()
        print(len(user_li))
        for user in user_li:
            number = user.number
            apiid = user.api_id
            apihash = user.api_hash
            print(number)
            try:
                client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        #             # pyrogram_authorization(number,apiid,apihash,client)

        #     #         # engagement_data = Engagements.objects.create(user = user)
                client.connect()
        #     #         if client.is_user_authorized():
                me = client.get_me()
        #     #             print(me.first_name)
                    
                p_client = Client(f'./sessions/{number}_p',api_id=f"{apiid}",api_hash=f"{apihash}",phone_number=str(number))
                p_client.connect()

                p_client.get_me()
                            
                p_client.disconnect()
        #         client.disconnect()
        # #         else:
        # #             inactive_user.objects.create(
        # #             user = user,
        # #             status = 'NOT AUTHORIZED'
        # #         )
        # #             user.status = "NOT AUTHORIZED"
        # #             user.save()
        # #             LOGGER.info(f'{number} is not authorized So please authorized it')    
            except p_errors.SessionPasswordNeeded as e:
                LOGGER.error(f'there {number} is SessionPasswordNeeded error')
                if not inactive_user.objects.filter(user=user).exists():
                    inactive_user.objects.create(
                        user = user,
                        status = 'NEED PASSWORD'
                    )
                user.status = 'NEED PASSWORD'
                user.save()
            except p_errors.PhoneNumberBanned as e:
                LOGGER.error(f'there {number} is PhoneNumberBanned error')
                if not inactive_user.objects.filter(user=user).exists():
                    inactive_user.objects.create(
                        user = user,
                        status = 'BANNED'
                    )
                user.status = 'BANNED'
                user.save()
            except p_errors.AuthKeyUnregistered as e:
                LOGGER.error(f'there {number} is AuthKeyUnregistered error')
                if not inactive_user.objects.filter(user=user).exists():
                    inactive_user.objects.create(
                        user = user,
                        status = 'NOT AUTHORIZED'
                    )
                user.status = 'NOT AUTHORIZED'
                user.save()
            except errors.AuthBytesInvalidError as e:
                LOGGER.error(f'there {number} is AuthBytesInvalidError error')
            except errors.FloodWaitError as e:
                LOGGER.error(f'there {number} is FloodWaitError error')
                if not inactive_user.objects.filter(user=user).exists():
                    inactive_user.objects.create(
                        user = user,
                        status = "TEMP BANNED"
                    )
                user.status = "TEMP BANNED"
                user.save()
            except errors.UserBannedInChannelError as e:
                LOGGER.error(f'there {number} is UserBannedInChannelError error')

                LOGGER.error('This user is banned from the channel / group')

            except Exception as e :
                client.disconnect()
                LOGGER.info(e)







        # aa = user_details.objects.exclude(status = "ACTIVE")
        # print(aa)

        # for user in aa:
        #     a = inactive_user.objects.create(
        #         user = user,
        #         status= user.status
        #     )
        #     print(a)








        count = 0
        succ_count = 0
        # for i in range(60):
        # for i in aa:
        #     user = i
        #     this_client = TelegramClient(f'./sessions/{user.number}',user.api_id,user.api_hash)
        #     this_client.connect() 
        #     try:
        #         this_client(JoinChannelRequest('pardeshi12311'))
        #         me = this_client.get_me()
        #         if this_client.send_read_acknowledge('pardeshi12311'):
        #             user.views += 1
        #             user.save()
        #             print(f"{me.first_name} have Marked as seen in {'pardeshi12311'}'s chat")
        #         else : 
        #             None
        #             print(f"{me.first_name} have No new messages in {'pardeshi12311'}'s chat")
        #         # this_client.send_message('pardeshi12311', 'Hi')
        #     except errors.FloodWaitError as e:
        #         user.status = "FLOOD WAIT"
        #         user.save()
        #         # e.seconds is how many seconds you have
        #         # to wait before making the request again.
        #         print('Flood for', e.seconds)
        #     except errors.UserBannedInChannelError as e:
        #         user.status = "BANNED"
        #         user.save()
        #         print('user is banned')
        #     except errors.ChatWriteForbiddenError as e:
        #         # user.status = "FLOOD WAIT"
        #         # user.save()
        #         print('user is banned to send message on chat')
        #     except errors.UserDeactivatedBanError as e:
        #         user.status = "DELETED"
        #         user.save()
        #         print('user is has been deleted')

        #     this_client.disconnect() 


            # if not this_client.is_user_authorized():
            #     try:
            #         this_client.send_code_request(user.number)
            #     except telethon.errors.rpc_error_list.PhoneNumberBannedError:
            #         print("Phone number is banned.")
            #         this_client.disconnect()
            # else:
            #     print('The user is authorised')
            # add_group('qatestingxana','qatestingxana',random.choice(COMMENTS_),user.number,user.api_id,user.api_hash)
