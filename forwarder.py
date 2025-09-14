import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaWebPage

# === এখানে আপনার তথ্য বসান ===
api_id = 20292708 # আপনার my.telegram.org থেকে পাওয়া API ID
api_hash = '715f27fbac8184833ef22e4132cca65a'  # আপনার API HASH

client = TelegramClient('forwarder.session', api_id, api_hash)

# সোর্স (auto signal) ও টার্গেট (ডেমো গ্রুপ) আইডি
SOURCE_CHANNEL_ID = -1001998961899  # যেখান থেকে সিগনাল ফরোয়ার্ড হবে
TARGET_GROUP_ID = -1002711701479   # ডেমো গ্রুপের আইডি (রিয়েল-টাইম)

# URL রিপ্লেসমেন্ট ফিচার সরানো হয়েছে

@client.on(events.NewMessage(chats=SOURCE_CHANNEL_ID))
async def forward_signal(event):
    try:
        # ৫ সেকেন্ড অপেক্ষা করুন
        await asyncio.sleep(5)
        
        # সব ধরনের মেসেজ forward করার জন্য - নিশ্চিত করছি প্রতিটি মেসেজ সেন্ড হবে
        message_sent = False
        
        if event.message.media:
            # Media type check করে WebPage media handle করো
            media_type = type(event.message.media).__name__
            
            if 'WebPage' in media_type:
                # WebPage media - শুধু text হিসেবে forward করো
                try:
                    await client.send_message(
                        TARGET_GROUP_ID, 
                        event.message.text or ""
                    )
                    print(f"✅ Real-time forwarded webpage message {event.message.id} to {TARGET_GROUP_ID}")
                    message_sent = True
                except Exception as text_error:
                    print(f"❌ Webpage text forwarding failed: {text_error}")
            else:
                # অন্য media - file হিসেবে forward করার চেষ্টা করো
                try:
                    await client.send_file(
                        TARGET_GROUP_ID,
                        file=event.message.media,
                        caption=event.message.text or "",
                        reply_markup=event.message.reply_markup
                    )
                    print(f"✅ Real-time forwarded media message {event.message.id} to {TARGET_GROUP_ID}")
                    message_sent = True
                except Exception as media_error:
                    # Media forward করতে না পারলে text হিসেবে forward করো
                    print(f"⚠️ Media failed, forwarding as text: {media_error}")
                    try:
                        await client.send_message(
                            TARGET_GROUP_ID, 
                            event.message.text or ""
                        )
                        print(f"✅ Real-time forwarded as text message {event.message.id} to {TARGET_GROUP_ID}")
                        message_sent = True
                    except Exception as text_error:
                        print(f"❌ Text forwarding also failed: {text_error}")
        
        if not message_sent:
            # যদি media না থাকে বা media/text forwarding fail হয়
            try:
                await client.send_message(
                    TARGET_GROUP_ID, 
                    event.message.text or "📨 Message forwarded"
                )
                print(f"✅ Real-time forwarded text message {event.message.id} to {TARGET_GROUP_ID}")
                message_sent = True
            except Exception as final_error:
                print(f"❌ All forwarding methods failed: {final_error}")
                # শেষ চেষ্টা - শুধু message ID পাঠাও
                try:
                    await client.send_message(TARGET_GROUP_ID, f"📨 Message {event.message.id} received but couldn't forward")
                    print(f"✅ Sent notification for message {event.message.id}")
                except:
                    print(f"❌ Complete failure for message {event.message.id}")
            
    except Exception as e:
        print(f"❌ Error forwarding: {e}")

async def main():
    print("🚀 Starting real-time signal forwarder...")
    print(f"📤 Source: {SOURCE_CHANNEL_ID}")
    print(f"📥 Target 1 (Real-time): {TARGET_GROUP_ID}")
    print("=" * 50)
    
    try:
        await client.start()
        print("✅ Bot started successfully!")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("💡 Try deleting forwarder.session file and run again")

if __name__ == "__main__":
    asyncio.run(main()) 