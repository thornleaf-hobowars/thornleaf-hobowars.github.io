import hobos from '../public/hobos.json'
import Head from "next/head"

export default function Page() {
    return <>
        <Head>
            <meta charSet="iso-8859-1" />
            <meta title="iso-8859-1" />
            <title>My page title</title>
        </Head>
        <h1>Hello, Next.js!</h1>
        <div>
            {Object.entries(hobos).map(([id, name], index) => (<div key={index}>{id}: <div dangerouslySetInnerHTML={{ __html: name }}></div>
                {escape(name)}</div>))}
        </div >
    </>
}