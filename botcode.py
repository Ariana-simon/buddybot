#Class Libraries 
#Library for creating Discord bots.
import discord 
#Library for interacting with the operating system.
import os
#Library for generating random numbers.
import random 
#Library for fetching EC2 metadata.
from ec2_metadata import ec2_metadata
#Library for loading environment variables from a file.
from dotenv import load_dotenv 

#Loading Discord bot token from the environment.
load_dotenv('token.env')
token = str(os.getenv('BOTTOKEN'))

#Creating Discord client instance with specific intents.
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#List of greeting messages.
#Creation of string array.
greet = ["hello","hey","hi"]

#Creation of function to print EC2 metadata.
#Function will print instance ID, instance type, and availability zone.
def print_ec2_metadata():
    try:
        instance_id = ec2_metadata.instance_id
        instance_type = ec2_metadata.instance_type
        availability_zone = ec2_metadata.availability_zone
        print(f"EC2 Instance ID: {instance_id}")
        print(f"Instance Type: {instance_type}")
        print(f"Availability Zone: {availability_zone}")
    except Exception as e: #If the function does not work an error message will be output.
        print(f"error fetching ec2 metadata: {e}")
print_ec2_metadata()#Call function to print EC2 metadata.

#Function to generate a random number for Picsum API.
def generate_random_number():
    return random.randint(1, 1000)

#Function to generate a random image URL from Picsum.
def get_random_image_url():
    random_number = generate_random_number()
    return f"https://picsum.photos/200/300?random={random_number}"
#Event handler for bot being ready.
@client.event
async def on_ready():
    print(f"logged in as{client.user}")

#Event handler for incoming messages.
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    content = message.content.lower()
    print(f'Message "{message.content}" by {message.author.name} in channel "{message.channel.name}"')
    if any(word in content for word in greet):#Bot will respond to any message with greetings in string.
        await message.channel.send(f"{random.choice(greet)} {message.author.mention}")#Bot will offer greeting and mention authors mention.
    elif "picture" in content or "image" in content:
        # If the message contains "picture" or "image", send a random image from Picsum
        image_url = get_random_image_url()
        await message.channel.send(image_url)
    elif "tell me about my server" in content:#Get EC2 metadata and send it to the discord channel. 
        instance_id = ec2_metadata.instance_id
        instance_type = ec2_metadata.instance_type
        availability_zone = ec2_metadata.availability_zone
        metadata_str = f"EC2 Instance ID: {instance_id}, Instance Type: {instance_type}, Availability Zone: {availability_zone}"
        # Send metadata information to the Discord channel
        await message.channel.send(metadata_str)
    

#Runs the Discord bot with the specified token.
client.run(token)
