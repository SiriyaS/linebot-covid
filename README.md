# linebot-covid
LINE messaging api with Flask

### linebot COVID-19 Tracker (only infection in Thailand)
## Setting Line Official Account
create your line messaging API in https://developers.line.me/

※ set **Auto-reply messages** to **Disable**

※ also **Enabled webhook**

※ copy your **Channel secret** and **Channel access token**

Ready to implement your code!

## Implement Line API
※ clone this repository
```
git clone https://github.com/SiriyaS/linebot-covid.git
```
cd to the project

※ set up virtual environment (if you don't have, install by `pip install virtualenv` first)
```
virtualenv -p python3 venv
```
※ activate the virtual environment
```
source venv/bin/activate
```
you can deactivate the virtual environment by type `deactivate` in terminal
※ install all dependencies in project
```
pip install -r requirements.txt
```
※ change **Channel secret** and **Channel access token** to yours

It's time to implement yor line API logic!

※ the logic for bot to answer the chat is in `function handle_message` 

※ the **text messeage** from the chat room is `event.message.text` variable

※ this line is how your linebot gonna answer (`reply_message` is the message your bot gonna answer)
```
line_bot_api.reply_message(
        event.reply_token,
        reply_message)
```
※ when you finish implementing the code **push** your work to your own **GitHub**

Next we gonna deploy our work to Heroku

## Deploy your code to Heroku
sign in to Heroku and **create new app**

※ for **Deployment Method** select **GitHub**

※ select **repository** and **branch** you want to connect with

※ for **Automatic Deploys** click **Enable Automatic Deploys** (if you want to deploy your work automatically whenever you push to GitHub)

※ (optional) for **Manual Deploy** click **Deploy branch**

Now, Let's connect Webhook to your linebot

## Add Webhook URL to your channel
Back to LINE Developer
In **Messaging API** tab goes down to **Webhook Setting**

※ add webhook URL ex. `https://<app_name>.herokuapp.com/webhook`

※ click **Verify** ,you should see **Success** pop-up window

🎉 Congratulation! Now your LINE bot is ready.

Add friend and start chatting.

