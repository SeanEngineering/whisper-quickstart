import './App.css';
import FileUpload01 from './components/file-upload-01';
import ResultsTable from './components/ResultsTable';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { mockData, columns } from '../mocks/data';

function App() {
  return (
    <div className='p-5'>
      <h1 className='text-3xl font-bold w-full flex'>Whisper Demo</h1>
      <div className='h-screen w-full flex py-5 gap-5'>
        <section className='w-[30%]'>
          <FileUpload01 />
        </section>
        <section className='w-[70%] flex flex-col gap-5'>
          <div className='flex gap-5'>
            <Input placeholder='Search for something...' />
            <Button className='w-[20%]'>Search</Button>
          </div>
          <section>
            <h1 className='text-2xl self-start flex'>Results</h1>
            <div>
              <ResultsTable data={mockData} columns={columns} />
            </div>
          </section>
        </section>
      </div>
    </div>
  );
}

export default App;
