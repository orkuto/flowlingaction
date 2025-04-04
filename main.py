import flowlingaction

a = flowlingaction.Maingame()

async def main():
    a.mainloop()
    await asyncio.sleep(0)


asyncio.run(main())
