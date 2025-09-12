import asyncio
from telethon import TelegramClient, events

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
        # ১ মিনিট (৬০ সেকেন্ড) অপেক্ষা করুন
        await asyncio.sleep(60)
        text = event.message.text or ""
        # URL রিপ্লেস করা হবে না - অরিজিনাল টেক্সট রাখা হবে
        if event.message.media:
            await client.send_file(
                TARGET_GROUP_ID,
                file=event.message.media,
                caption=text
            )
            print(f"✅ Real-time forwarded media message {event.message.id} to {TARGET_GROUP_ID}")
        elif text:
            await client.send_message(TARGET_GROUP_ID, text)
            print(f"✅ Real-time forwarded text message {event.message.id} to {TARGET_GROUP_ID}")
        else:
            print(f"⚠️ Unknown message type: {event.message.id}")
    except Exception as e:
        print(f"❌ Error forwarding: {e}")

print("🚀 Starting real-time signal forwarder...")
print(f"📤 Source: {SOURCE_CHANNEL_ID}")
print(f"📥 Target 1 (Real-time): {TARGET_GROUP_ID}")
print("=" * 50)

client.start()
client.run_until_disconnected() 