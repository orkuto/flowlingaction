import flowlingaction

async def main():
    a = flowlingaction.Maingame()
    a.mainloop()
    await asyncio.sleep(0)


asyncio.run(main())