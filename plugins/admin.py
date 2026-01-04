"""
管理员管理插件

提供通过聊天指令动态添加或移除机器人管理员的功能。
"""
from core.bot import Bot
from core.command_manager import matcher
from core.admin_manager import admin_manager
from models.events.message import MessageEvent

__plugin_meta__ = {
    "name": "管理员管理",
    "description": "管理机器人的全局管理员",
    "usage": (
        "/admin list - 列出所有管理员\n"
        "/admin add <QQ号> - 添加管理员\n"
        "/admin remove <QQ号> - 移除管理员"
    ),
}


@matcher.command("admin", permission=MessageEvent.ADMIN)
async def handle_admin_command(bot: Bot, event: MessageEvent, args: list[str]):
    """
    处理 /admin 指令

    :param bot: Bot 实例
    :param event: 消息事件实例
    :param args: 指令参数列表
    """
    if not args:
        await event.reply(__plugin_meta__["usage"])
        return

    action = args[0].lower()

    if action == "list":
        admins = await admin_manager.get_all_admins()
        if not admins:
            await event.reply("当前没有设置任何管理员。")
            return
        
        admin_list_str = "\n".join(str(admin_id) for admin_id in admins)
        await event.reply(f"当前管理员列表 ({len(admins)}):\n{admin_list_str}")
        return

    if action in ("add", "remove"):
        if len(args) < 2 or not args[1].isdigit():
            await event.reply("参数错误，请提供一个有效的 QQ 号。\n示例: /admin add 123456")
            return

        try:
            user_id = int(args[1])
        except ValueError:
            await event.reply("无效的 QQ 号，请输入纯数字。")
            return

        if action == "add":
            success = await admin_manager.add_admin(user_id)
            if success:
                await event.reply(f"成功添加管理员: {user_id}")
            else:
                await event.reply(f"管理员 {user_id} 已存在，无需重复添加。")
            return
        
        elif action == "remove":
            success = await admin_manager.remove_admin(user_id)
            if success:
                await event.reply(f"成功移除管理员: {user_id}")
            else:
                await event.reply(f"管理员 {user_id} 不存在。")
            return

    await event.reply(f"未知的指令: {action}\n\n{__plugin_meta__['usage']}")
