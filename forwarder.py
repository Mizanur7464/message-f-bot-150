import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaWebPage

# === এখানে আপনার তথ্য বসান ===
api_id = 24607929 # আপনার my.telegram.org থেকে পাওয়া API ID
api_hash = '6d7028e6aec86b06e4524439c4a8394b'  # আপনার API HASH

client = TelegramClient('forwarder.session', api_id, api_hash)

# সোর্স (auto signal) ও টার্গেট (ডেমো গ্রুপ) আইডি
SOURCE_CHANNEL_ID = -1001998961899  # যেখান থেকে সিগনাল ফরোয়ার্ড হবে
TARGET_GROUP_ID = -1002711701479   # ডেমো গ্রুপের আইডি (রিয়েল-টাইম)

# URL রিপ্লেসমেন্ট ফিচার সরানো হয়েছে

@client.on(events.NewMessage(chats=SOURCE_CHANNEL_ID))
async def forward_signal(event):
    try:
        # ২৫ সেকেন্ড অপেক্ষা করুন
        await asyncio.sleep(25)
        
        # সব ধরনের মেসেজ forward করার জন্য
        if event.message.media:
            # Media সহ মেসেজ
            try:
                # প্রথমে media হিসেবে forward করার চেষ্টা করো
                await client.send_file(
                    TARGET_GROUP_ID,
                    file=event.message.media,
                    caption=event.message.text or "",
                    reply_markup=event.message.reply_markup
                )
                print(f"✅ Real-time forwarded media message {event.message.id} to {TARGET_GROUP_ID}")
            except Exception as media_error:
                # Media forward করতে না পারলে text হিসেবে forward করো
                print(f"⚠️ Media failed, forwarding as text: {media_error}")
                await client.send_message(
                    TARGET_GROUP_ID, 
                    event.message.text or "", 
                    reply_markup=event.message.reply_markup
                )
                print(f"✅ Real-time forwarded as text message {event.message.id} to {TARGET_GROUP_ID}")
        else:
            # শুধু text মেসেজ
            await client.send_message(
                TARGET_GROUP_ID, 
                event.message.text or "", 
                reply_markup=event.message.reply_markup
            )
            print(f"✅ Real-time forwarded text message {event.message.id} to {TARGET_GROUP_ID}")
            
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