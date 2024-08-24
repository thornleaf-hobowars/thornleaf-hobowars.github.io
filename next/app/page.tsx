import hobos from '../public/hobos.json'

export default function Page() {
    return <><h1>Hello, Next.js!</h1>
        <div>
            {Object.entries(hobos).map(([id, name]) => <div>{id}: {name.normalize("NFD")}</div>)}
        </div>
    </>
}