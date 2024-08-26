export default async function Page() {
    // This fetch will run on the server during `next build`
    const fs = require('fs/promises')
    console.log(await fs.readFile('public/hobos.json'))
    // const res = await fetch('/')
    // const data = await res.json()

    return <main dangerouslySetInnerHTML={{ __html: (await fs.readFile('public/hobos.json')).toString('latin1') }}></main >
}