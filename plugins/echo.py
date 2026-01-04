"""
Echo 与交互插件

提供 /echo 和 /赞我 指令。
"""
from core.command_manager import matcher
from core.bot import Bot
from models import MessageEvent

__plugin_meta__ = {
    "name": "echo",
    "description": "提供 echo 和 赞我 功能",
    "usage": "/echo [内容] - 复读内容\n/赞我 - 让机器人给你点赞",
}

@matcher.command("echo")
async def handle_echo(bot: Bot, event: MessageEvent, args: list[str]):
    """
    处理 echo 指令，原样回复用户输入的内容

    :param bot: Bot 实例
    :param event: 消息事件对象
    :param args: 指令参数列表
    """
    if not args:
        reply_msg = "请在指令后输入要回复的内容，例如：/echo 你好"
    else:
        reply_msg = " ".join(args)

    await event.reply(reply_msg)

@matcher.command(
    "赞我",
    permission=MessageEvent.ADMIN,
    override_permission_check=True
)
async def handle_poke(bot: Bot, event: MessageEvent, permission_granted: bool):
    """
    处理 赞我 指令，发送点赞

    :param bot: Bot 实例
    :param event: 消息事件对象
    :param permission_granted: 权限检查结果
    """
    if not permission_granted:
        await event.reply("只有我的操作员才能让我点赞哦！(｡•ˇ‸ˇ•｡)")
        return

    try:
        # 尝试发送赞
        await bot.send_like(event.user_id, times=10)
        await event.reply("好感度+10！(〃'▽'〃)")
    except Exception as e:
        await event.reply(f"点赞失败了 >_<: {str(e)}")